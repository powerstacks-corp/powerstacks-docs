---
title: "App catalog and cloud packaging"
description: "Browse WinGet packages, publish to Intune with PSADT wrapping, manage ring-based updates, and configure auto-deploy."
---

# App catalog and cloud packaging

The **App Catalog** tab in the Admin Dashboard lets you browse over 9,000 apps from Microsoft's official WinGet repository ([microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs)) and publish them directly to Intune as Win32 apps. Package manifests are fetched directly from GitHub (no third-party services), ensuring zero supply chain attack risk.

### Browsing the App Catalog

1. Go to **Admin** > **App Catalog** tab
2. Popular packages are displayed 24 per page with pagination controls
3. Use the search box to find specific apps (search uses "Load More" infinite scroll)
4. Each package shows: name, publisher, version, and description
5. Icons are loaded automatically where available

### Publishing to Intune

1. Find the app you want to publish
2. **Select architecture and locale** (if available):
   - Each package card displays available architectures (e.g., x64, x86, arm64) and locales (e.g., en-US, de-DE, fr-FR)
   - If multiple options are available, they appear as dropdown selectors
   - If only one option is available, it appears as a label showing what will be published
   - Default selections: x64 for architecture, en-US for locale
3. Select the **Publish to Intune** button on the package card
4. A packaging job is created with your selected architecture and locale
5. Monitor job status in the **Packaging Jobs** section below the catalog

**Architecture, locale, and version tracking:**

When apps are published from the WinGet catalog:

- The selected architecture, locale, and version are stored in the packaging job
- When the app is synced from Intune, it automatically inherits these values
- Deployment groups are named to include all three: `AppStore-AppName-x64-en-US-v25-10-186-0-Required`
- Dots in version numbers are replaced with dashes (e.g., `25.10.186.0` becomes `v25-10-186-0`)
- This helps identify which variant and version of multi-architecture apps is deployed, and prevents duplicate deployments of the same version

### Packaging jobs

The Packaging Jobs section shows all queued and completed packaging operations:

| Status | Description |
|--------|-------------|
| **Pending** | Job is queued, waiting for processing |
| **Downloading** | Downloading the installer from WinGet manifest URL |
| **Packaging** | Wrapping in PSADT v4 and creating .intunewin package |
| **Uploading** | Uploading package to Intune via Graph API |
| **Creating** | Creating Win32LobApp in Intune |
| **Completed** | App successfully created in Intune |
| **Failed** | Error occurred - select Retry to requeue |

### Packaging architecture

The packaging process runs in-process on the App Service, no separate containers, agents, or functions needed:

1. **Queue message**: When you select "Publish to Intune", a job is added to Azure Storage Queue
2. **Background service**: The in-process `PackagingQueueService` picks up the job
3. **Download**: Installer is downloaded from the URL in the WinGet manifest
4. **Wrapping** (PSADT mode only): Installer is wrapped in PSAppDeployToolkit v4 for standardized deployment
5. **Package creation**: `.intunewin` package is created using the cross-platform SvRooij.ContentPrep library
6. **Intune upload**: The package is uploaded and a Win32LobApp is created via Graph API

### Packaging methods: Raw vs PSADT

When publishing an app from the App Catalog, you can choose between two packaging methods using the dropdown on each package card:

| Method | Description |
|--------|-------------|
| **Raw** (default) | Packages the installer directly. The installer executable is the entry point, Intune runs it with silent switches. Simpler, smaller package size. |
| **PSADT** | Wraps the installer in [PSAppDeployToolkit v4](https://psappdeploytoolkit.com/). Provides standardized logging, pre/post-install hooks, and consistent exit codes across all installer types. Larger package size due to framework files. |

**When to use PSADT:**

- You need standardized deployment logging across all apps
- You want consistent install/uninstall behavior regardless of installer type
- You need the pre-installation and post-installation hooks (e.g., closing running applications before install)

**When to use Raw:**

- You want the simplest, most direct installation
- Package size matters (PSADT adds ~5 MB of framework files)
- The app's native installer already handles silent installation well

#### Raw packaging details

In Raw mode, the installer is packaged directly into the `.intunewin` file. The install and uninstall commands sent to Intune depend on the installer type:

**Install commands by file type:**

| File Type | Install Command | Uninstall Command |
|-----------|----------------|-------------------|
| `.msi` | `msiexec /i "installer.msi" {silent switch}` | `msiexec /x "installer.msi" {silent switch}` |
| `.exe` | `"installer.exe" {silent switch}` | Registry lookup (see below) |
| `.msix` / `.appx` | `powershell.exe Add-AppxPackage -Path 'installer.msix'` | Registry lookup (see below) |

**Registry-based uninstall (for non-MSI):** For EXE and other non-MSI installers, the uninstall command searches the Windows registry (`HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall` and the `Wow6432Node` equivalent) for an entry matching the app's display name. It uses the `QuietUninstallString` if available, otherwise appends `/S /silent /quiet` to the `UninstallString`.

#### PSADT packaging details

In PSADT mode, the installer is placed inside a PSAppDeployToolkit v4 folder structure. The PSADT framework provides a standardized wrapper around the installer with logging, error handling, and consistent exit codes.

**Package structure created:**

```
Package/
+-- Invoke-AppDeployToolkit.exe       <-- Entry point (what Intune runs)
+-- Deploy-Application.ps1            <-- Generated install/uninstall logic
+-- AppDeployToolkit/                 <-- Framework files (from PSADT v4 template)
|   +-- AppDeployToolkitMain.ps1
|   +-- AppDeployToolkitHelpers.ps1
|   +-- ...
+-- Files/
    +-- installer.exe (or .msi)       <-- Your actual installer
```

**Intune commands (all PSADT packages use the same commands):**

- **Install:** `Invoke-AppDeployToolkit.exe -DeploymentType Install -DeployMode Silent`
- **Uninstall:** `Invoke-AppDeployToolkit.exe -DeploymentType Uninstall -DeployMode Silent`

**Generated Deploy-Application.ps1 script variables:**

| Variable | Value |
|----------|-------|
| `$appVendor` | Publisher name from the WinGet manifest |
| `$appName` | Package name from the WinGet manifest |
| `$appVersion` | (empty, version tracked via Intune metadata) |
| `$appLang` | `EN` |
| `$appRevision` | `01` |
| `$appScriptVersion` | `1.0.0` |
| `$appScriptAuthor` | `AppRequestPortal` |

**Install section, what runs during installation:**

For **MSI** installers:

```powershell
Execute-MSI -Action Install -Path "$dirFiles\installer.msi"
```

PSADT automatically adds `/qn /norestart` when running in Silent deploy mode. If a custom silent switch was provided that includes MSI properties (e.g., `TRANSFORMS=...`, `PROPERTY=VALUE`), those are passed via `-AddParameters`.

For **EXE** installers:

```powershell
Execute-Process -Path "$dirFiles\installer.exe" -Parameters '{silent switch}' -WaitForMsiExec
```

The `-WaitForMsiExec` parameter ensures PSADT waits if another MSI installation is already in progress. EXE installers always get explicit silent switches since PSADT doesn't know the correct flags for each installer.

**Uninstall section, what runs during uninstallation:**

For **MSI** installers:

```powershell
Execute-MSI -Action Uninstall -Path "$dirFiles\installer.msi"
```

For **non-MSI** installers, the script searches the registry for the app's uninstall string:

```powershell
$regPaths = @(
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$app = Get-ItemProperty $regPaths |
    Where-Object { $_.DisplayName -like '*AppName*' } |
    Select-Object -First 1

if ($app.QuietUninstallString) {
    Execute-Process -Path 'cmd.exe' -Parameters "/c $($app.QuietUninstallString)"
} elseif ($app.UninstallString) {
    Execute-Process -Path 'cmd.exe' -Parameters "/c $($app.UninstallString) /S /silent /quiet"
}
```

**Repair section:** Runs the same commands as the install section. PSADT supports `Invoke-AppDeployToolkit.exe -DeploymentType Repair -DeployMode Silent` for reinstallation.

**Error handling:** If the PSADT script encounters a fatal error, it exits with an error code in the 60000 range and logs the error details. PSADT's built-in logging writes to `C:\Windows\Logs\Software\` on the target device.

The following PSADT error codes are mapped as "Failed" return codes in Intune:

| Exit Code | Description |
|-----------|-------------|
| `60001` | General PSADT error (catch block in Deploy-Application.ps1) |
| `60002` | Error during pre-installation phase |
| `60003` | Error during installation phase |
| `60008` | Generic non-zero exit from the wrapped installer |

These are registered in the Intune Win32 app return code mappings so that PSADT failures are properly reported in Intune and reflected in the portal's install status tracking.

**PSADT fallback:** If PSADT wrapping fails for any reason (e.g., template download failure, extraction error), the system automatically falls back to Raw packaging. The job will still complete successfully, just without the PSADT wrapper.

**PSADT template caching:** The PSADT v4 template is downloaded once from the [official GitHub releases](https://github.com/PSAppDeployToolkit/PSAppDeployToolkit/releases) and cached in Azure Blob Storage (`psadt-template/PSAppDeployToolkit_Template_v4.zip`). Subsequent packaging jobs reuse the cached template.

#### Silent switches

Silent switches tell the installer to run without displaying any UI. The portal resolves the silent switch in this order:

1. **WinGet manifest value**, if the manifest specifies `InstallerSwitches.Silent`, that value is used
2. **Installer type default**, based on the `InstallerType` field in the WinGet manifest
3. **File extension fallback**, based on the installer's file extension
4. **Last resort**, `/S /silent`

**Default silent switches by installer type:**

| Installer Type | Silent Switch | Used By |
|---------------|--------------|---------|
| **MSI** / **WiX** | `/qn /norestart` | Windows Installer packages |
| **InnoSetup** | `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-` | Inno Setup installers |
| **Nullsoft** / **NSIS** | `/S` | NSIS installers |
| **Burn** | `/quiet /norestart` | WiX Burn bootstrapper bundles |
| **EXE** (generic) | `/S /silent` | Generic executables |

These defaults are applied in both Raw and PSADT modes.

#### Detection scripts

Every app published to Intune includes an auto-generated PowerShell detection script. Intune runs this script on target devices to determine whether the app is already installed.

**Detection strategy (in order of preference):**

1. **ProductCode detection (most reliable)**, if the WinGet manifest includes `AppsAndFeaturesEntries` with a `ProductCode` (MSI GUID), the script checks for that exact GUID in the registry uninstall paths. This is the most precise detection method.

2. **DisplayName detection (fallback)**, if no ProductCode is available, the script searches the registry for an entry where `DisplayName` matches the app name (using wildcard matching). Publisher name is also checked if available in the manifest.

**Version checking:** When a version number is available from the WinGet manifest (via `AppsAndFeaturesEntries.DisplayVersion` or the package version), the detection script compares the installed version against the required minimum version. Apps with older versions are reported as "Not Installed" so Intune will upgrade them.

**Registry paths checked:**

- `HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*`
- `HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*`

**Script execution context:** Detection scripts run as 64-bit PowerShell (`runAs32Bit: false`) without signature enforcement (`enforceSignatureCheck: false`). The script exits with code `0` if the app is detected, or `1` if not installed.

#### Intune Win32 app configuration

When the app is created in Intune via the Graph API, the following settings are applied:

| Setting | Value |
|---------|-------|
| **Applicable architectures** | x64, x86 |
| **Minimum OS** | Windows 10 1903 |
| **Install context** | System (runs as SYSTEM account) |
| **Device restart behavior** | Based on return code |

**Return codes configured:**

| Code | Type | Meaning |
|------|------|---------|
| `0` | Success | Installation completed successfully |
| `1707` | Success | Installation completed successfully (MSI) |
| `3010` | Soft reboot | Installation succeeded, reboot recommended |
| `1641` | Hard reboot | Installation succeeded, reboot initiated |
| `1618` | Retry | Another installation is in progress, retry later |

**App icon:** If available, the app icon is fetched automatically (via Google S2 Favicon API or GitHub publisher avatar) and included as a PNG or JPEG in the Intune app metadata.

### Setting up packaging

Packaging works out of the box with the default deployment. No additional setup is required beyond:

1. **Azure Storage account** (deployed by default via Bicep template)
2. **Graph API permissions** for Intune app management (see Prerequisites)
3. **Verify connectivity**:
   - Go to Admin > App Catalog
   - Try publishing a test app (e.g., "7-Zip")
   - Check Packaging Jobs for status

The PSADT v4 template is automatically downloaded from the [official GitHub repository](https://github.com/PSAppDeployToolkit/PSAppDeployToolkit) on first use and cached in Azure Blob Storage.

### Manifest integrity verification

By default, the packaging pipeline trusts WinGet manifests fetched from `raw.githubusercontent.com`. Each manifest declares a SHA256 for its installer, and the pipeline verifies the downloaded installer matches before publishing to Intune. That defends against a tampered installer at the publisher's download server, but it does not defend against a tampered *manifest* on the GitHub fetch path.

To close that gap, enable **Settings → "Verify manifest integrity against Microsoft's signed index"**.

When the setting is enabled:

1. Before packaging any WinGet-sourced app, the portal downloads Microsoft's signed community index (`source2.msix`, ~10 MB) from `https://cdn.winget.microsoft.com/cache/source2.msix`.
2. The portal extracts the SQLite database embedded in that MSIX and looks up the package by its identifier.
3. If the package is not present in the index, the packaging job fails immediately with an explicit *"Manifest integrity check failed"* error. There is no silent fallback.
4. The downloaded MSIX and extracted SQLite are cached for 12 hours to avoid re-downloading the index on every packaging job.

**When to enable this:** Any environment that wants the same manifest-trust posture as the WinGet client itself. The cost is a one-time ~10 MB download every 12 hours and a brief extra step on the first packaging job after a cache refresh.

**When to leave it off:** If you've already implemented your own integrity controls (e.g. a hardened internal mirror of the WinGet repo with its own signing pipeline) and prefer to rely on those.

**Failure mode:** If verification fails for a specific package, only that packaging job fails, other jobs continue normally. To temporarily bypass verification (for example, to package a package that is genuinely missing from the index due to an upstream removal), an admin can disable the setting from the Settings page and retry. Re-enable it afterward.

For the full security chain and v2 roadmap (per-version manifest hash comparison, MSIX signature validation), see [Security Overview](security.md).

### App updates

The **App Updates** tab in the Admin Dashboard shows all apps that have been published from WinGet and are being tracked for version updates.

**Tracked apps table:**

| Column | Description |
|--------|-------------|
| **App** | App name and publisher |
| **WinGet Package ID** | The WinGet identifier (e.g., `Microsoft.VisualStudioCode`) |
| **Published Version** | Version currently in your portal/Intune |
| **Latest Version** | Latest version available in the WinGet repository |
| **Status** | Steady state for this app, **Update Available**, **Up to Date**, **Unknown** (sticky, when the last deploy attempt failed), or **Check failed** (sticky, when the most recent WinGet update lookup couldn't resolve a version). *Unknown* is intentionally non-alarming, when packaging or assignment fails, we genuinely don't know what state Intune is in until you investigate via the activity bell or the Packaging Jobs tab. Transient deploy progress (Queued, Packaging, Assigning, etc.) is surfaced in the **activity bell** at top-right of the admin pages, not in this column. |
| **Ring Template** | Name of the ring template configured for this app, or "—" when the app uses custom rings or ringless mode (per-app settings live in the Update Ring Configuration side panel) |
| **Last Checked** | When the version was last compared. A small red dot is shown when the most recent check failed (e.g., the WinGet package ID could not be resolved) |
| **Actions** | Deploy Update or Dismiss (only shown when update is available). **Deploy Update** opens a confirmation wizard showing exactly what will be deployed (app, version, ring mode, target, ring breakdown, auto-deploy setting) before you commit. |

Select any row in the table to open a per-app detail view where you can configure ring deployment, set the auto-deploy override, and run an immediate update check (**Check Now**) just for that app, useful when you want to confirm a single app's status without waiting for the next scheduled run.

**Automatic tracking:**

- Apps published from the WinGet catalog are automatically tracked for updates
- The `SourceWingetPackageId` is backfilled automatically by the background service (no manual Intune sync required)
- Update checks run on a configurable schedule (default: every hour when enabled)
- The "Last Checked" date now stamps on every attempt, success or failure, so a stale date in the UI tells you "this app's lookup has been failing", not "the service is broken". The failure reason is shown on the per-app detail view under **Last Check Result**.

**Actions:**

- **Check for Updates**: Manually trigger an update check for all tracked apps
- **Check Now** (per-app, on the detail view): Run an update check for a single app without waiting for the schedule
- **Deploy Update**: Opens a confirmation wizard (v1.24.0+) showing the deployment summary, app, version transition, ring mode (template/custom rings/ringless), ring breakdown or ringless target+filter, and the per-app auto-deploy override. Once you select **Deploy** in the wizard, a packaging job is queued that downloads the new version from WinGet, wraps it in PSADT, archives the `.intunewin` to blob storage for rollback, creates a new Install Win32 app in Intune (advancing the portal's version pointer) and a paired Update Win32 app with a requirement script that targets only devices already running the app. Watch the activity bell at top-right for in-flight progress.
- **Dismiss**: Hides the update notification for that app

**Activity bell (v1.24.0+):**

The bell icon at the top-right of every admin page is an Intune-style task tracker. The badge shows the count of in-flight deploys plus any sticky-failed entries; select the bell to open a drawer listing recent activity with each entry's current state, age, and any error or pause message. Adaptive polling: 15 seconds while at least one task is in-flight, 60 seconds otherwise to keep the badge accurate; stops entirely when nothing's happening and the drawer is closed (so you're not burning API calls just to show a zero badge). Use this when you need to know *what's happening right now* across all your deploys; use the App Updates Status column when you need to know *what state each app is in*; use the **Activity tab** (below) when you need the full historical timeline.

**Dismissing sticky failures (v1.27.0+):**

Each terminal entry in the bell drawer (Up-to-Date, Packaging Failed, Assignment Failed) has a × dismiss button. Dismissing removes the entry from the drawer's default view and from the Activity Log tab's default view. Active entries, Queued, Packaging, Assigning, Paused, can't be dismissed; they're still moving and would just reappear on the next poll. A new failure for the same app is a distinct row, so a re-failure shows up regardless of whether you dismissed the prior one. Dismissals persist per-browser via `localStorage`. To restore everything you've dismissed, open the **Activity** tab and select *Restore dismissed*.

**Activity tab (v1.27.0+):**

Full unified timeline of packaging jobs and update deployments, the same data the bell drawer surfaces, but with no terminal-entry cap. Use this when you need to answer "what happened last week" or "did this app's last three deploys all fail?", questions the 8-entry drawer can't span.

The filter bar above the activity table:

- **State**, All / Active (in flight) / Failed / Up-to-Date / Paused
- **Time**, Last 24 hours / 7 days / 30 days / 90 days / All time (default 30 days)
- **Search**, free-text match against app name and version
- **Show dismissed**, toggle to include entries you've dismissed in the bell drawer

Filters compose. The table paginates at 25 rows per page so a long history doesn't bog the page down. Each row has its own *Dismiss* button mirroring the bell drawer's behaviour, plus the standard state badge, started/finished timestamps, and the deploy's error or pause message.

The **Run cleanup** button on this tab runs both retention sweeps in one action:

- Packaging jobs older than 30 days (keeping the 100 most-recent)
- Update deployments older than 90 days (keeping the 100 most-recent)

In-flight and Paused work is never deleted regardless of age, and the most-recent N rows are always preserved regardless of age. Cleanup is manual, there is no scheduled background sweep, so retention happens on whatever cadence admins choose.

The bell drawer's footer link **View all activity →** deep-links straight here (`/admin?tab=activity`).

**Recovery for stuck or orphaned deploys (v1.24.0+):**

If a deploy gets stuck (e.g., App Service restart killed the worker mid-packaging) or completes packaging but the Update app handler doesn't advance the deployment, the recovery action is reachable from either side of the same orphaned state:

- **Packaging Jobs table** surfaces **Cancel and Cleanup** for in-flight stuck jobs and **Cleanup orphaned deploy** for completed jobs whose linked deployment is still on Packaging.
- **Update Deployments table** (v1.26.0+) surfaces a parallel **Cancel and Cleanup** for deployments stuck on Packaging.

Both routes call the same `cancel-and-cleanup` endpoint: one action marks the packaging job Failed for audit, marks the linked deployment Failed, and deletes the per-job blob folder to free storage. The Cleanup actions are time-gated to deployments that have been stuck for more than 10 minutes, brand-new deployments legitimately sit at Packaging for a few minutes while the Update-app handler runs, so the button is hidden until the threshold is exceeded. Re-trigger the deploy from **App Updates → Deploy Update** when ready, the new attempt starts clean.

### Update Ring Templates

Ring templates define a staged deployment strategy for app updates. Instead of deploying an update to all devices at once, rings let you roll out to a pilot group first, wait a configurable number of days, then expand to broader groups.

**Managing templates:**

In **Admin** > **Settings**, scroll to the **Update Ring Templates** section:

- Select **Create Template** to define a new ring template
- Each template has a name and one or more rings (up to 10)
- Each ring has a name (e.g., "IT Pilot"), a delay in days, and one or more Microsoft Entra ID security groups
- Each ring has its own deployment settings: available/deadline timing, install behavior, restart settings, notifications, and delivery optimization
- Select **Show Deployment Settings** on any ring to configure available time (days + time of day), deadline time, restart grace period, snooze settings, and more
- Ring 1 typically has a 0-day delay (deploys immediately); subsequent rings deploy after their configured delay
- Set one template as the **default** to auto-assign it to new apps
- Select **Import from Autopatch** to discover Windows Autopatch ring groups from your Microsoft Entra ID and pre-populate rings with those groups

**Example configuration:**

| Ring | Name | Delay | Groups |
|------|------|-------|--------|
| 1 | IT Pilot | 0 days | IT-Pilot-Devices |
| 2 | Early Adopters | 3 days | Early-Adopters |
| 3 | Production | 7 days | All-Managed-Devices |

This means Ring 1 deploys immediately, Ring 2 deploys 3 days later, and Ring 3 deploys 7 days after Ring 2, a total rollout of 10 days.

**Per-app configuration:**

For apps published from the WinGet catalog, select the app's row on the **App Updates** tab to open its detail view. The detail view includes an **Update Rings** section with three deployment styles:

- **Ringless**, updates deploy immediately to a single Intune assignment with no staged rollout. Pick **All Devices** or **All Users** as the target (default: All Devices), and optionally apply an Intune assignment filter to narrow the audience (e.g. limit by OS version or department). Ringless still creates the same two-app Install/Update pair as ringed mode (so rollback, install/update telemetry, and the lifecycle Status column work identically), it just collapses the rollout to a single ring targeting the chosen built-in audience.
- **Use a template**, apply a reusable ring template defined under **Update Ring Templates**. If a default template is set, it is preselected.
- **Custom rings**, define rings specific to this one app. Same per-ring controls as a template (groups, availability/deadline timing, install behavior, restart settings, end-user notifications, delivery optimization, assignment filter), scoped to a single app. Use this when no global template fits, for example when this app needs a different pilot group, a different rollout pace, or a specific assignment filter.

When you select **Custom rings**, choose **Edit custom rings** to open the ring editor. Edits in the editor are held in the side panel until you select **Save**, switching between deployment styles before saving doesn't lose your in-progress custom rings. Ringless target/filter choices are likewise preserved when you flip to a ringed mode and back, so admins can experiment without losing prior settings.

The detail view also has an **Auto-Deploy Updates** section to set the per-app override (use the global default, always auto-deploy, or never auto-deploy). As of v1.23.0 auto-deploy works for ringless apps too, the only safety check is that the **Update Ring Configuration** side panel has been opened at least once for the app (so the admin has explicitly picked ringed *or* ringless mode rather than leaving it unconfigured).

> **Note (v1.20.0):** The Update Rings and Auto-Deploy controls used to live on the App Management tab's app detail view. They have moved to the App Updates tab because not every app under App Management is tracked for updates, only apps published from the WinGet catalog are.

### Ring-based deployments

When you select **Deploy Update** for an app with ring-based updates enabled, the system:

1. Creates a packaging job for the new version (same as non-ringed updates)
2. When packaging completes, creates a new "Update" Win32 app in Intune
3. Activates **Ring 1** immediately, creates Required assignments for Ring 1's groups
4. Schedules subsequent rings based on their configured delays
5. A background service checks every 15 minutes for rings that are ready to activate
6. When each ring's delay expires, its groups receive the Required assignment

**Deployment dashboard:**

The **App Updates** tab shows active and recent deployments below the updates table:

- **Ring progress indicator**, colored circles show which ring is active
- Select a deployment row to expand and see detailed ring status, schedule dates, and group assignments
- **Pause**, stops ring progression (active ring stays deployed, next ring is held)
- **Resume**, restarts ring progression after a pause
- **Advance**, manually skip the delay for the next ring (useful for accelerating after pilot validation)
- **Halt rollout**, removes active ring assignments and marks the deployment rolled back. Devices that already updated keep the new version; future rings are stopped. (Renamed from *Rollback* in v1.26.0 to disambiguate from the App-level rollback that swaps the Install app back to the prior version on all devices.)
- **Cancel**, removes all assignments and marks the deployment as canceled
- **Cancel and Cleanup**, for deployments stuck on Packaging for more than 10 minutes. Marks the deployment Failed, marks the linked packaging job Failed, and deletes the blob folder for that job in one atomic action. Mirrors the *Cancel and Cleanup* button on the Packaging Jobs table.

**Two-app model:**

When you deploy an update, **ringed *or* ringless** (v1.23.0+), the system creates two separate Win32 apps in Intune:

1. **Install app** (user-targeted) -- immediately updated to the new version so new installs always get the latest. Existing assignments are preserved.
2. **Update app** -- a separate Win32 app with a requirement script that only installs on devices that already have the app. Devices without the app see it as "Not Applicable." Assignments are created on this app:
   - In **ringed** mode, one Required assignment per group per ring, activated as the rollout progresses.
   - In **ringless** mode, a single Required assignment to **All Devices** or **All Users** (the admin's choice in the Update Ring Configuration side panel), with an optional Intune assignment filter. Created and activated immediately at deploy time, there's only one ring to roll out.

This separation ensures:

- New device enrollments always get the latest version (no vulnerability window)
- Updates to existing devices are controlled separately from new installs (and, in ringed mode, gated through rings with health checks)
- User-targeted and device-targeted assignments don't conflict

**Per-ring assignment settings:**

When a ring activates, the per-ring deployment settings configured on the template are applied to the Intune assignment. Each ring's assignment includes:

- **Available time** -- computed from the ring activation time plus the ring's "Available after days" + "Available at time" (or "as soon as possible" if not configured)
- **Deadline time** -- computed the same way for the install deadline (or none if not configured)
- **Time zone** -- assignment uses device local time when "Use device time zone" is enabled, otherwise UTC
- **End user notifications** -- Show all, Show reboot only, or Hide all
- **Delivery optimization priority** -- Foreground or Not configured
- **Restart settings** -- grace period, countdown, and snooze duration (omitted when restart behavior is "Suppress")
- **Assignment filter** -- optional Intune filter (Include or Exclude) scoping the ring to a subset of devices

Settings are read from the deployment-time snapshot on the ring, so changes to the template after a deployment starts do not affect rings already in flight.

**Per-ring assignment filters:**

Each ring in a template can target an Intune assignment filter. Open the ring's "Show Deployment Settings" panel and pick a filter from the list (Windows-platform filters from your tenant). Choose **Include matching devices** or **Exclude matching devices**, or clear the filter to assign without one. The filter is snapshotted onto the deployment ring at deploy time alongside the other ring settings.

**Install app rollback:**

If a new version has installation issues, you can roll back the Install app to the previous version in one action. In the app detail view, the **Version and Rollback** section card (top of the Properties view, v1.26.0+) has a primary **Roll back to previous version** button. This swaps the Install app back to the previous version's Intune app (which still exists in Intune), so new installs receive the older working version. No re-packaging is needed.

To pick a specific historical version (rather than the immediate predecessor), select **View full history…** in the same section card. The version history modal lists every published version with archive status and a per-version Rollback button.

**Update app rollback:**

Rolling back a ring-based deployment removes the Intune assignments from active rings so no additional devices receive the update. Devices that already installed the update retain the new version -- Intune does not uninstall it.

### Signal-based ring progression

Ring advancement is not just delay-based -- the system checks device install health from Intune before advancing to the next ring. This prevents a failed update from rolling out broadly.

**How it works:**

After a ring's delay expires, the progression service queries Intune for device install status before advancing:

| Condition | Action |
|-----------|--------|
| Success rate >= threshold (default 95%) | Advance to next ring |
| Failure rate > failure threshold (default 10%) | **Auto-pause** deployment, notify admin |
| Not enough data yet (evaluation period not met) | Wait, even if delay expired |

**Configuration (on ring templates):**

| Setting | Default | Description |
|---------|---------|-------------|
| Minimum success rate | 95% | Required success rate before advancing |
| Maximum failure rate | 10% | Failure rate that triggers auto-pause |
| Minimum evaluation period | 24 hours | Wait time after ring activation before checking status |

Set the minimum success rate to 0% to advance based on delay only (disables health checks).

### Auto-deploy updates

Updates can be deployed automatically when detected, eliminating the need to select "Deploy Update" for each app.

**Global setting (Admin > Settings):**

- **Auto-deploy updates** -- when enabled, all apps with ring-based updates configured will automatically package and deploy through their rings when a new version is detected

**Per-app override (App detail view):**

- **Always auto-deploy** -- this app always auto-deploys, regardless of the global setting
- **Never auto-deploy** -- this app never auto-deploys, regardless of the global setting
- **Use global default** -- follows the global setting

**Safety requirements:**

- Auto-deploy only works for apps with ring-based updates enabled. Apps without rings configured will still require manual "Deploy Update" actions, even if auto-deploy is on. This ensures all auto-deployed updates go through staged rings.
- The "Deploy Update" button on the Updates tab always works for manual one-off deployments regardless of auto-deploy settings.

### WinGet integration settings

In **Admin** > **Settings** > **WinGet Integration**:

| Setting | Description |
|---------|-------------|
| **WinGet Repository URL** | GitHub repository URL for WinGet packages. Default: `https://github.com/microsoft/winget-pkgs` (Microsoft's official repository). Format: `https://github.com/owner/repo` or `owner/repo`. Organizations with custom/private WinGet repositories can point to their internal GitLab/GitHub mirror. **Warning**: Changing this will clear the entire package cache. |
| **GitHub Personal Access Token** | Recommended. Required for the "Show More Results" live search feature (GitHub's Code Search API requires authentication). Also increases API rate limits from 60/hour to 5,000/hour for faster cache syncs. Create a classic token at [https://github.com/settings/tokens](https://github.com/settings/tokens) with `public_repo` scope. |

#### Why use a GitHub token?

**Without token** (unauthenticated):

- 60 API requests per hour
- Initial cache sync takes 2-3 hours
- May hit rate limits during heavy use
- **"Show More Results" live search will not work**, GitHub's Code Search API requires authentication. Only cached results and exact package ID lookups (e.g., `Google.Chrome`) will return results.

**With token** (authenticated):

- 5,000 API requests per hour
- Initial cache sync takes 30-60 minutes
- Reliable operation even with many users
- **Full live search**, "Show More Results" queries the entire WinGet repository in real time via GitHub Code Search, finding packages that may not yet be in the local cache

**Creating a GitHub personal access token:**

1. Go to [GitHub Settings → Personal Access Tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Select "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name: "App Store for Intune WinGet Integration"
4. Select scope: **public_repo** (Access public repositories)
5. Select "Generate token"
6. Copy the token (starts with `ghp_...`)
7. Paste into Admin Settings → WinGet Integration → GitHub Personal Access Token
8. Select Save Settings

**Note**: Tokens are stored securely in Azure Key Vault and never exposed in logs or UI.

### Local development testing

For developers testing the packaging feature locally:

1. **Prerequisites**:
   - Azure Storage account configured (uses the same storage queue and blob container as production)
   - Graph API credentials configured for Intune access

2. **Configure the API** (`src/AppRequestPortal.API/appsettings.json`):
   - Ensure `AzureStorage:ConnectionString` points to your Azure Storage account

3. **Run the services**:
   ```bash
   # API with background packaging service (port 5000)
   cd src/AppRequestPortal.API && dotnet run

   # Frontend (port 3000)
   cd src/AppRequestPortal.Web && npm start
   ```

4. **Test**: Go to Admin > App Catalog, search for an app, select "Publish to Intune". The in-process background service will pick up the job and process it.

### Troubleshooting packaging

**Jobs stuck in Pending:**

- Verify the App Service is running and the background service started (check Application Insights logs for `PackagingQueueService`)
- Ensure the `AzureStorage:ConnectionString` is configured correctly
- Check that the storage queue `packaging-jobs` exists

**Jobs failing during download:**

- The service downloads directly from the installer URL in the WinGet manifest
- Check if the package exists in the Microsoft winget-pkgs repository
- Review logs for HTTP errors or GitHub API rate limits

**Jobs failing during PSADT wrapping:**

- PSADT wrapping has graceful fallback, if it fails, the raw installer is packaged instead
- Check logs for `PsadtService` entries
- First-time use requires downloading the PSADT template from GitHub; ensure outbound HTTPS is allowed

**Jobs failing during upload:**

- Verify the API has Graph API permissions for Intune (`DeviceManagementApps.ReadWrite.All`)
- Review API logs for Graph API errors (detailed error messages are logged)
