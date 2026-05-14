---
title: "App Management"
description: "Manage the Intune app catalog: sync apps, configure visibility and approvals, edit deployment settings, and roll back versions."
---

# App Management

The App Management tab is your central hub for managing which Intune apps are available in the portal and how they behave.

### Syncing Apps from Intune

1. Click the **Sync Apps from Intune** button
2. The portal fetches all mobile apps from your Intune tenant
3. Apps are imported with their name, publisher, description, icon, and category
4. New apps are hidden by default - you must make them visible for users to see them

**Incremental Sync:** After the first full sync, subsequent syncs are incremental, only new and modified apps are fetched from Intune. The portal tracks the last sync date and uses `lastModifiedDateTime` filtering to minimize Graph API calls. Icons are fetched in parallel (5 concurrent requests) for faster sync times.

**Scheduled Background Sync:** A background service automatically syncs apps on a schedule:

- **Nightly full sync** at 2:00 AM UTC, catches deletions and ensures consistency
- **Hourly incremental sync**, picks up new and changed apps quickly
- The manual **Sync Apps from Intune** button is still available for on-demand syncs

**Pagination:** The portal follows `@odata.nextLink` pagination from the Graph API, so tenants with more than 999 apps are fully supported.

### Filtering the App List

The filter bar above the app table has six axes (v1.26.0+). All filters compose with the search box and persist while you navigate the tab:

| Filter | Values | Default |
|--------|--------|---------|
| **Platform** | All / Windows / iOS / Android / macOS / Web (only platforms present in your tenant) | All |
| **Visibility** | All / Visible / Hidden | All |
| **Category** | All / *(per-tenant categories)* | All |
| **Source** | All / Store / Intune | All |
| **Purpose** | Install / Update / All | Install |
| **Search** | Free-text match against app name and publisher | empty |

**Source** distinguishes apps published through the App Store catalog flow (where the portal owns the lifecycle) from apps that already existed in Intune and were synced into the portal. *Source = Store* shows only apps with `sourceWingetPackageId` set, these are the apps where Version and Rollback, ring-based update deployments, and the Publish wizard apply.

**Purpose** distinguishes the user-facing **Install** Win32 app from the paired **Update** Win32 app that drives the two-app update model. The default is *Install* so the table shows the user-facing apps you'd expect; flip to *Update* when you need to inspect Update apps directly (for example to verify an Update app's group assignments or ring activation state). The flag is set automatically during Intune sync by joining against `UpdateDeployment.UpdateIntuneAppId`, there is no manual classification step.

### App Table Columns

The app list table is read-only and informational. Click any row to open the app's detail view where you can edit settings.

| Column | Description |
|--------|-------------|
| **App** | App name, icon, and publisher |
| **Platform** | App platform badge (Windows, iOS, Android, macOS, Web) |
| **Type** | App type from Intune (e.g., Win32, Microsoft Store, iOS Store) |
| **Assigned** | Status badge showing whether a target group is configured (Yes/No/N-A) |
| **Visible** | Status badge showing whether users can see this app in the portal (Yes/No/N-A) |
| **Approval** | Status badge showing whether approval is required (Yes/No/N-A) |
| **Date Added** | When the app was first synced or published |

### Supported App Types

The portal supports self-service deployment for specific app types. When syncing apps from Intune, each app is classified by platform and support status:

| Platform | Supported Types | Unsupported Types |
|----------|-----------------|-------------------|
| **Windows** | Win32, Microsoft Store (New) | Windows Universal (LoB), MSI (LoB), AppX (LoB) |
| **iOS** | iOS Store, iOS VPP | iOS (LoB) |
| **Android** | Android Store, Managed Google Play, Android for Work | Android (LoB) |
| **Web** | Web Apps | - |
| **macOS** | - | All macOS app types |

**Why some types are unsupported:**

- **Line of Business (LoB) apps** require special handling during deployment that the portal cannot automate
- **macOS apps** have different deployment mechanisms that are not yet implemented

Unsupported apps appear in the admin UI with their type displayed and an "N/A" status badge. Admins can see these apps exist but cannot make them available for self-service.

### Configuring Individual Apps

Click any app row in the table to open its **detail view**. The detail view has two sections accessible from the left navigation:

- **Overview**, quick summary cards showing platform, visibility, approval status, assignment type, date added, and version
- **Properties**, grouped property sections (described below), each with an **Edit** link

#### Editing App Settings

There are three ways to edit app settings from the detail view:

1. **Side panel (quick edit)**, click "Edit" on the Visibility or Approval section to open a slide-out panel for fast single-field changes
2. **Settings wizard**, click "Edit" on the Assignment or Deployment Options section to open the full 5-step wizard, starting at the relevant step
3. **Edit All Settings**, click the "Edit All Settings" button to open the wizard from step 1

The **App Settings Wizard** has 5 steps:

| Step | Title | Fields |
|------|-------|--------|
| 1 | Visibility and Store | Visible, Featured, Category, Cost |
| 2 | Approval | Requires Approval, Acknowledgment |
| 3 | Assignment | Assignment type, Target group, Assignment filter |
| 4 | Deployment Options | Install behavior, Restart behavior, Notifications, Grace period (Win32 only) |
| 5 | Review + Save | Summary of all changes with diff highlighting |

#### Visibility Settings

- **Yes**: App appears in the user-facing app catalog
- **No**: App is hidden from users but still tracked in the system
- **N/A**: App type is not supported for self-service deployment

Use this to control which Intune apps are available for self-service requests. Apps that shouldn't be requested (system apps, dependencies, etc.) should remain hidden.

**Hiding Apps with Active Deployments:**

When you set an app's visibility to **No** and it has an active Intune deployment and Azure AD group, a confirmation dialog appears asking whether you also want to delete the deployment group and assignment:

- **OK**: Hides the app AND removes the Intune assignment and deletes the Azure AD deployment group
- **Cancel**: Only hides the app but preserves the deployment infrastructure (useful if you plan to make it visible again later)

> **Note:** Deleting the deployment and group is permanent. Users who currently have the app will lose access when group membership is removed.

**Automatic Deployment Setup:**

When you set an app's visibility to **Yes** for the first time, the portal automatically:

1. **Creates an Entra ID Security Group** named `{GroupNamePrefix}{AppName}-{arch}-{locale}-v{version}-Required`
   - Example: `AppStore-Microsoft Teams-x64-en-US-v1-0-0-Required`
   - The prefix is configurable in Settings (default: `AppStore-`)
   - Dots in version numbers are replaced with dashes (e.g., `1.0.0` becomes `v1-0-0`)

2. **Creates an Intune App Assignment**
   - The app is assigned as **Required** to the new security group
   - Assignment type (User or Device) is based on the app's Assignment setting

This automation ensures that when a user's request is approved, they simply need to be added to the group and Intune handles the deployment.

> **Note:** If group or assignment creation fails, the error is logged but the visibility change still succeeds. You can manually create the assignment in Intune if needed.

#### Approval Settings

- **Yes**: Requests go through the configured approval workflow before completion
- **No**: Requests are auto-approved and the user/device is immediately added to the target group
- **N/A**: App type is not supported

Approval can only be enabled for visible apps. If you try to enable approval for a hidden app, you'll see a warning: "App must be visible in the store to enable approval."

#### Delete from Intune

From the app detail view, apps with a real Intune deployment (not synced apps with a `winget-` prefix) can be deleted. This removes the app from both Intune and the portal entirely.

**Confirmation flow:**

1. **Step 1**, "Are you sure you want to delete *[app name]* from Intune?"
   - Click **Delete** to proceed, or **Cancel** to abort
2. **Step 2** *(only for portal-published apps with a deployment group)*, "This app has a deployment group (*group name*). Do you also want to delete the deployment group?"
   - Click **Yes** to delete the group, or **No** to keep it for reuse when republishing

**What gets deleted:**

| Action | Always | Only if "Yes" to group deletion |
|--------|--------|-------------------------------|
| Win32 app removed from Intune | Yes | — |
| Intune assignment removed | Yes | — |
| All associated requests removed | Yes | — |
| App record removed from portal | Yes | — |
| Entra ID security group deleted | — | Yes |

After deletion, the app is completely removed from the portal. To restore it, republish from the WinGet catalog.

**When to use Delete from Intune:**

- You need to republish an app with updated settings (e.g., different silent switches, updated installer)
- An app deployment is in a bad state and needs to be recreated
- You want to permanently remove an app from both Intune and the portal

### Edit App Modal

Click **Edit** on any app row to open the Edit App Modal, which provides access to all configurable app properties:

#### App Details Section

| Field | Description |
|-------|-------------|
| **Cost** | Optional cost to display on app cards (informational only, no billing). Enter a decimal value or leave empty for "Free". |
| **Category** | App category displayed on app cards. Start typing to see suggestions from existing categories in your catalog. You can enter any category name. |

#### Assignment Settings Section

| Field | Description |
|-------|-------------|
| **Assignment Type** | User (add requester to group) or Device (add requester's device to group) |
| **Target Group** | Entra ID security group for app assignment. Click "Search Groups" to browse, or use "Clear" to remove. |
| **Assignment Filter** | Optional Intune assignment filter. Select filter type (Include/Exclude) and choose a filter. |

#### Win32 Deployment Options Section

These options appear only for Win32 apps and control Intune deployment behavior:

| Field | Description |
|-------|-------------|
| **Install Context** | System (machine-wide) or User (per-user) installation |
| **Device Restart** | How to handle restart after install: Based on Return Code, Allow, Suppress, or Force |
| **End User Notification** | What users see: Show All, Show Reboot Only, or Hide All |
| **Allow Available Uninstall** | Whether users can uninstall from Company Portal |
| **Restart Grace Period** | Enable/configure grace period before forced restart |

Click **Save** to apply changes or **Cancel** to discard.

#### App Icon

Each app displays an icon in the catalog. Icons are typically synced from Intune, but some apps may be missing icons. The Edit App modal provides two ways to set an icon:

- **Upload Icon**, upload a PNG or JPEG image file from your computer
- **Browse Library**, opens the Icon Library picker, which shows all unique icons already used by other apps in the portal. Search by app name or publisher, then click an icon to apply it instantly. This is useful when multiple apps share the same publisher icon or when you want to reuse an existing icon without re-uploading.

#### Assignment Type

Determines what gets added to the Entra ID group when a request is approved:

- **User**: The requesting user is added to the group (most common)
- **Device**: The user's device is added to the group (useful for device-targeted deployments)

For Device assignment:

- The portal **auto-detects** the user's current device based on browser/OS information
- Devices matching the detected OS are pre-selected in the dropdown
- The user can override the selection if they want to install on a different device
- If a primary device is set in Intune and matches the current OS, it takes priority
- The selected device is added to the target AAD group
- Intune deploys the app to that specific device

**Device Detection Logic:**

1. Browser detects the operating system (Windows, macOS, iOS, Android)
2. Portal matches against the user's registered Intune devices
3. Matching devices are marked as "(Detected)" in the dropdown
4. A helpful message confirms the auto-detection: "This device was automatically detected based on your current browser."

### Configuring Approval Workflows

Click the **Workflow** button on any app to open the Approval Workflow Editor.

#### No Approval Required

For apps with "Approval" set to "No", requests are auto-approved immediately. No workflow configuration is needed.

#### Simple Approval

For apps that just need someone from the Approver Group to sign off:

1. Set "Approval" to "Yes"
2. Leave the workflow with no stages
3. Any member of the configured Approver Group can approve

#### Manager + Additional Approvers

1. Enable **Require Manager Approval**
2. Choose workflow type:
   - **Linear**: Specific users approve in sequence
   - **Pooled**: Any member of specified groups can approve
3. Add approval stages as needed

#### Conditional Stages (v1.8.2)

Each approval stage can be made conditional, so it only applies when specific criteria are met:

1. Open the Approval Workflow Editor for an app
2. Add a stage and assign an approver or group
3. Toggle "Make this stage conditional"
4. Add conditions using the condition builder:
   - Select a condition type (Department, Cost Center, Job Title, Location, Platform, Request Count)
   - Choose an operator (Equals, Not Equals, Contains, etc.)
   - Enter the comparison value
5. Add multiple conditions with AND/OR logic
6. A human-readable summary of the conditions is shown on the stage card

See [Approval Workflows](approval-workflows.md) for detailed condition types and operators.

See [Approval Workflows](approval-workflows.md) for detailed workflow configuration options.

### Version History and Rollback

The portal tracks version history for apps published from the App Catalog, so you can roll back to previous versions if a new version introduces issues.

#### Viewing Version History

1. Go to **Admin** > **App Management** tab
2. Find the app in the app table
3. Open the app's detail view by clicking the row
4. The Version History modal displays all recorded versions

#### Understanding Version Status

Each version in the history shows a status badge:

| Status | Description |
|--------|-------------|
| **Current** (blue) | The version currently deployed in Intune |
| **Archived** (gray) | Previous version that was deployed, available for rollback |
| **Failed** (red) | Deployment or publish attempt that failed |

#### Version Information Displayed

For each version, you'll see:

- **Version number** - The semantic version (e.g., "1.2.3")
- **Recorded date** - When this version was detected/published
- **Updated by** - User who published this version (if available)
- **Installer size** - Size of the installer package
- **Release notes** - Change summary for this version
- **Package ID** - WinGet package identifier (e.g., "7zip.7zip")

#### Rolling Back to a Previous Version

If a new app version causes issues, you can roll back to a previous version:

1. Open the **Version History** modal for the app
2. Find the version you want to roll back to (must have "Archived" status)
3. Click the **Rollback** button on that version
4. Click **Confirm Rollback** to proceed
5. The portal will:
   - Re-publish the selected version to Intune
   - Update the app assignment with the older version
   - Mark the rolled-back version as "Current"
   - Archive the previously current version

> **Important:** Rollback is only available for versions marked as "Archived". Failed deployments and the current version cannot be rolled back to.

#### Version History Limitations

- **Winget apps only**: Version history is only tracked for apps published from the App Catalog
- **Manual Intune apps**: Apps added directly to Intune (not via portal) do not have version history
- **Retention policy**: By default, the portal keeps all versions indefinitely. Admins can configure retention limits in Settings

#### Troubleshooting Rollback Issues

**Rollback button is grayed out:**

- Only "Archived" versions can be rolled back to
- Ensure the version's installer is still available

**Rollback fails:**

- Check Graph API permissions (`DeviceManagementApps.ReadWrite.All`)
- Verify the installer URL is still accessible
- Review API logs for detailed error messages

**Version history is empty:**

- Version history only tracks apps published through the portal
- If you synced an existing Intune app, its pre-sync versions are not tracked
- Only new publishes/updates will appear in history
