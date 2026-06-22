---
title: "Configure PSADT via Intune ADMX"
description: "Standardize PSADT v4 behavior across your fleet by ingesting PSADT's official ADMX template into Intune as a Configuration Profile. Recommended baseline settings included."
---

# Configure PSADT via Intune ADMX

App Store for Intune wraps every package with PowerShell App Deployment Toolkit (PSADT) v4 before handing it to Intune. PSADT has its own configuration surface, things like log paths, dialog timeouts, auto-silent detection, and per-installer-type behavior — and PSADT v4.1 ships an official ADMX template covering that whole surface.

The recommended way to manage PSADT settings tenant-wide is to ingest that ADMX into Microsoft Intune as a Configuration Profile. Settings push to your devices through the standard Intune policy CSP, the same channel Intune uses for everything else. No GPO, no on-premises Active Directory, no custom tooling.

This page walks through the ingestion flow, plus a recommended baseline you can apply on day one.

## What you get

Once the Configuration Profile is in place, every PSADT-wrapped install on every targeted device picks up the policy values. That includes:

- Where PSADT writes its logs (co-locate with the Intune Management Extension logs for one-stop log harvesting)
- How long PSADT waits for user response before falling back to silent install
- When PSADT should detect "no user logged in" and run unattended automatically (the Autopilot ESP case, scheduled deployments, etc.)
- Default MSI install parameters PSADT passes to `msiexec`
- Dialog timeouts, restart-prompt cadence, deferral behavior, language, fluent vs classic UI default, and roughly 25 other knobs

The full setting reference lives in the [PSADT v4 documentation](https://psappdeploytoolkit.com/docs/reference/functions/Get-ADTConfig). This guide covers the policies most worth setting and the Intune-specific ingestion flow.

## How App Store packages interact with these settings

PSADT's configuration precedence is **ADMX/registry > per-package `config.psd1` > PSADT defaults**.

App Store's packaging pipeline hardcodes one setting at the per-package layer: `Toolkit.LogPath` is set to `C:\ProgramData\Microsoft\IntuneManagementExtension\Logs` in every package's `config.psd1` at wrap time, so PSADT logs land in the IME folder regardless of whether the ADMX policy is in place. If you set `Toolkit.LogPath` via ADMX to a different value, the ADMX policy wins and your value applies. That's the right precedence: tenant-wide admin intent should override individual package defaults.

Everything else PSADT can be configured for is unset at the per-package layer. PSADT's bundled defaults apply unless you set an ADMX policy.

## Prerequisites

- Microsoft Intune tenant with permission to create Configuration Profiles (Intune Service Administrator or higher).
- Windows 10/11 devices enrolled in Intune. The PSADT ADMX template targets Windows.
- The latest PSADT v4 release. Download from [github.com/PSAppDeployToolkit/PSAppDeployToolkit/releases](https://github.com/PSAppDeployToolkit/PSAppDeployToolkit/releases). The `.admx` and `.adml` files are in the `PolicyDefinitions` folder of the release ZIP.

## Step 1: Download the PSADT ADMX template

1. Open the [PSADT releases page](https://github.com/PSAppDeployToolkit/PSAppDeployToolkit/releases) and download the latest v4.x release ZIP.
2. Extract the ZIP locally.
3. Inside the extracted release, find the `PolicyDefinitions` folder. You're looking for two files:
   - `PSAppDeployToolkit.admx` (the template itself)
   - `en-US\PSAppDeployToolkit.adml` (the English language strings file; PSADT also ships translations in sibling locale folders if you need them)

Keep both files handy. You'll upload them in Step 2.

## Step 2: Ingest the ADMX into Intune

1. Sign in to the [Microsoft Intune admin center](https://intune.microsoft.com).
2. Go to **Devices** → **Configuration** → **+ Create** → **New policy**.
3. **Platform:** Windows 10 and later.
4. **Profile type:** Templates.
5. From the template list, pick **Imported Administrative templates (Preview)**.
   !!! note "Why this profile type"
       Intune supports several ADMX-flavored profile types. "Imported Administrative templates" is the one that lets you bring your own third-party ADMX. The "Administrative templates" type (without "Imported") is for Microsoft's pre-loaded set and won't let you upload PSADT's.
6. Select **Create**.
7. On the **Basics** page, give the policy a name like `PSADT Configuration - Baseline` and an optional description. Select **Next**.
8. On the **Configuration settings** page, select **Add** and upload the `PSAppDeployToolkit.admx` file from Step 1.
9. When prompted, also upload `PSAppDeployToolkit.adml` from the `en-US` folder.
10. Select **Next** to continue once the upload completes. The PSADT settings tree appears in the left-side tree view of the Configuration settings page.

## Step 3: Configure the recommended baseline

Most of the PSADT settings are off-by-default ("Not configured" in the Configuration Profile). Setting them explicitly is what makes them apply tenant-wide.

The following baseline is the set we recommend starting with. Every setting has a sensible PSADT default; the rationale column explains why we recommend setting it explicitly anyway.

| ADMX setting | Recommended value | Why |
|---|---|---|
| `Toolkit.LogPath` | `C:\ProgramData\Microsoft\IntuneManagementExtension\Logs` | Co-locates PSADT logs with IME logs and msiexec logs. One Graph `collectDiagnostics` call grabs all three streams in a single zip. App Store packages already write to this path; setting the ADMX policy brings non-App-Store PSADT packages into alignment too. |
| `Toolkit.CompressLogs` | Enabled | Zips PSADT's log output at the end of each install. One zip per package instead of dozens of loose `.log` files. Makes support escalations cleaner. |
| `Toolkit.OobeDetection` | Enabled | PSADT runs unattended automatically during Autopilot Enrollment Status Page (ESP). Without this, PSADT can prompt during ESP and stall provisioning. |
| `Toolkit.SessionDetection` | Enabled | Auto-Silent when no interactive user is logged in. Catches scheduled deployments and devices in the middle of the night without forcing every install to be configured Silent per-package. |
| `Toolkit.ProcessDetection` | Enabled | Auto-Silent when none of the target processes (e.g., the app being installed) are running. Skips the close-running-apps prompt when there's nothing to close. |
| `UI.DefaultTimeout` | 1200 | Twenty minutes is a reasonable response window for user-facing prompts. The PSADT default is similar; setting this explicitly locks it. |
| `UI.DefaultPromptPersistInterval` | 60 | Re-prompt cadence for unattended prompts, in seconds. One minute is a balance between "user notices the dialog" and "user not annoyed." |
| `UI.RestartPromptPersistInterval` | 300 | Restart prompts re-prompt every five minutes. Restart prompts are more disruptive than regular ones; longer cadence reduces user friction. |
| `MSI.InstallParams` | `/qn REBOOT=ReallySuppress` | Locks the default MSI parameters. PSADT applies these globally to every `msiexec` call. Locking via policy prevents a misconfigured package from issuing a reboot mid-deployment. |

Set each one to **Enabled** and enter the recommended value (or the equivalent toggle, depending on the setting type). Leave any setting you're not sure about as **Not configured**; PSADT's bundled default applies.

When you're done, select **Next** to continue.

## Step 4: Scope tags (optional)

If you use scope tags, apply them now. Otherwise select **Next** to skip.

## Step 5: Assign to devices

1. On the **Assignments** page, choose **+ Add groups** and target the device group(s) you want the policy applied to. For a first rollout, target a pilot group (a handful of devices) so you can verify behavior before going broader.
2. After validating with the pilot, edit the assignment and switch the target to your full Windows estate or whichever scope matches your deployment-ring strategy.
3. Select **Next**, review the policy summary, and **Create** to finalize.

Intune syncs the policy to assigned devices on the next check-in (typically within 8 hours; a manual `Sync` from the Company Portal or device settings forces it immediately).

## Verifying the policy is applied

On a target device, after the policy syncs:

1. Open Registry Editor as administrator.
2. Browse to `HKLM\Software\Policies\PSAppDeployToolkit` (or its WOW6432Node equivalent on 32-bit reads).
3. You should see the values you set in the Configuration Profile.
4. Trigger a PSADT-wrapped install from Intune. PSADT reads the policy values at runtime; logs land at the configured `Toolkit.LogPath` and behavior follows the configured settings.

If the registry keys aren't present, check the device's MDM diagnostic logs (`%ProgramData%\Microsoft\IntuneManagementExtension\Logs\IntuneManagementExtension.log`) for the policy fetch result. Most "missing policy" issues come down to assignment scope or sync timing.

## What this doesn't cover

The ADMX template reaches every setting in PSADT's `config.psd1`. It does not reach two layers that live inside each individual package:

1. **Per-package asset files** (banner images, app icons, dark-mode logos). Those are bundled into the `.intunewin` at wrap time and can't be ADMX-driven.
2. **`strings.psd1` overrides** (the user-facing text in PSADT dialogs). Same reason: strings live inside each package.

Both are on the App Store for Intune roadmap as in-portal customization features. For now, customers who need either can either fork PSADT's templates with their own assets/strings before App Store wraps them, or wait for the in-portal customization UI.

## Cross-references

- [App Catalog and Cloud Packaging](app-catalog-cloud-packaging.md) — how App Store wraps each package with PSADT before deploying.
- [Troubleshooting](troubleshooting/index.md) — log locations and diagnostic flows. PSADT logs end up in the same folder as IME logs once `Toolkit.LogPath` is set per the baseline above.
- [PSADT v4 Configuration Reference](https://psappdeploytoolkit.com/docs/reference/functions/Get-ADTConfig) (external) — full setting reference for every value you can configure via ADMX.
