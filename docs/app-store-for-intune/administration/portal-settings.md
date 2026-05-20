---
title: "Portal settings"
description: "Configure portal-wide options: authorization, display, deployment, version management, license, and custom domains."
---

# Portal settings

The Settings tab lets you configure portal-wide options including authorization, display settings, deployment configuration, and version management. Notification and messaging settings are on the **Communications** tab (see [Communications](communications.md)).

### Group-based authorization

Control who has admin and approver access to the portal.

| Setting | Description |
|---------|-------------|
| **Admin Group** | **(Required)** Entra ID group Object ID. Members have full admin access to sync apps, manage settings, and view all requests. **If not configured, all admin endpoints return 403 Forbidden.** |
| **Approver Group** | Entra ID group Object ID. Members can approve/reject requests (in addition to workflow-specific approvers) |

> **Important (v1.10.6+):** The Admin Group is **required**. If no Admin Group ID is configured (in either portal settings or `appsettings.json`), all users are denied admin access. See the [Setup Guide](../installation/setup-guide/) for initial configuration instructions.
>
> **Lost admin access?** If the Admin Group ID is accidentally cleared from portal settings, the `appsettings.json` / environment variable value is used as a fallback. If neither is set, you must set `AppSettings__AdminGroupId` as an environment variable (or in `appsettings.json`) and restart the application to regain access.

### Recommended Conditional Access policy

Since the App Store for Intune is used to request apps for Intune-managed devices, we recommend protecting access to the portal with a Conditional Access policy that requires:

- **Managed device** - The device accessing the portal must be enrolled in Intune
- **Compliant device** - The device must meet your organization's compliance policies

This ensures users can only request apps from trusted, compliant devices.

#### Prerequisites

Before creating the policy:

1. You must have **Entra ID Premium P1** or **P2** license (or Microsoft 365 E3/E5, etc.)
2. You need the **Conditional Access Administrator** or **Global Administrator** role
3. Have at least one compliance policy configured in Intune

#### Creating the Conditional Access policy

1. **Go to Conditional Access**
   - Go to [Azure Portal](https://portal.azure.com)
   - Go to **Microsoft Entra ID** > **Security** > **Conditional Access**
   - Select **+ New policy**

2. **Name the policy**
   - Enter a descriptive name: `App Store for Intune - Require Compliant Device`

3. **Configure Assignments - Users**
   - Under **Users**, select **0 users and groups selected**
   - Select **Include** > **All users**
   - (Optional) Under **Exclude**, add a break-glass admin account for emergency access

4. **Configure Assignments - Target Resources**
   - Under **Target resources**, select **No target resources selected**
   - Select **Cloud apps**
   - Select **Include** > **Select apps**
   - Search for and select your App Store for Intune app registrations:
     - `App Store for Intune API` (or your API app registration name)
     - `App Store for Intune Frontend` (or your frontend app registration name)
   - Select **Select**

5. **Configure Conditions (optional)**
   - Under **Conditions** > **Device platforms**
   - Select **Not configured**
   - Set **Configure** to **Yes**
   - Select **Include** > **Select device platforms**
   - Check: **Windows**, **iOS**, **Android** (the platforms you manage)
   - Select **Done**

6. **Configure Access Controls - Grant**
   - Under **Grant**, select **0 controls selected**
   - Select **Grant access**
   - Check **Require device to be marked as compliant**
   - Check **Require Microsoft Entra hybrid joined device** (optional, for hybrid environments)
   - Select **Require one of the selected controls** (OR) or **Require all the selected controls** (AND) based on your requirements
   - Select **Select**

7. **Configure Session Controls (optional)**
   - Under **Session**, you can configure:
     - **Sign-in frequency**: Require re-authentication periodically
     - **Persistent browser session**: Disable persistent sessions for extra security

8. **Enable the policy**
   - Set **Enable policy** to **Report-only** first to test
   - Select **Create**

9. **Test and enable**
   - Monitor the Sign-in logs for a few days in Report-only mode
   - Verify legitimate users can access the portal from compliant devices
   - Verify access is blocked from non-compliant/unmanaged devices
   - Once verified, edit the policy and change to **On**

#### Policy summary

| Setting | Value |
|---------|-------|
| **Name** | App Store for Intune - Require Compliant Device |
| **Users** | All users (exclude break-glass account) |
| **Cloud apps** | App Store for Intune API, App Store for Intune Frontend |
| **Conditions** | Device platforms: Windows, iOS, Android |
| **Grant** | Require device to be marked as compliant |
| **Enable policy** | Report-only (then On after testing) |

#### Troubleshooting access issues

If users report they cannot access the portal:

1. **Check Sign-in logs**
   - Go to **Microsoft Entra ID** > **Sign-in logs**
   - Filter by the user and application
   - Look for **Failure** entries and check the **Conditional Access** tab
   - The tab shows which policies applied and why access was denied

2. **Common issues**

   | Issue | Solution |
   |-------|----------|
   | Device not enrolled | User needs to enroll their device in Intune |
   | Device not compliant | User needs to resolve compliance issues (updates, encryption, etc.) |
   | Using personal device | User needs to use their work-managed device |
   | Policy excluding wrong users | Review the Exclude settings in the CA policy |

3. **Verify device status**
   - Go to **Microsoft Intune admin center** > **Devices**
   - Search for the user's device
   - Check **Compliance** status and any failed compliance policies

#### Alternative: Allow browser access with app protection

If you need to allow browser access from unmanaged devices (less secure), you can create an alternative policy:

1. Create a second CA policy for browser access
2. Target the same apps
3. Under **Conditions** > **Client apps**, select **Browser** only
4. Under **Grant**, require **Approved client app** or **App protection policy**
5. This allows access from unmanaged devices but with some protection

> **Recommendation:** For maximum security, require compliant managed devices. The App Store for Intune is designed for employees requesting apps on their managed devices, so this policy aligns with the intended use case.

### General settings

| Setting | Description |
|---------|-------------|
| **Require manager approval by default** | When enabled, new approval workflows include manager approval as the first stage |
| **Auto-create Entra ID groups** | Automatically create a security group when an app doesn't have a target group configured |

### Version and updates

The Settings tab displays version information and update settings:

| Setting | Description |
|---------|-------------|
| **Current Version** | Displays the installed portal version, build date, and environment |
| **Automatically check for updates** | When enabled, the portal periodically checks for new versions |
| **Show update notifications** | When enabled, displays a notification banner when updates are available |
| **Check for Updates** | Manual button to check for available updates |
| **Install Update** | One-click button to download and install updates (requires configuration) |

When an update is available, you'll see:

- Update badge with the new version number
- Link to release notes
- **Install Update** button (if auto-update is configured)

#### Enabling in-app updates

The portal supports one-click updates directly from the Admin Dashboard. This feature downloads the latest release and deploys it via Azure's Kudu ZIP deploy API.

**Prerequisites:**

- Portal must be running in Azure App Service
- Deployment credentials must be configured

**Configuration steps:**

1. **Get deployment credentials** from Azure Portal:
   - Go to your App Service → **Deployment Center** → **FTPS credentials**
   - Copy the **Username** (starts with `$`, e.g., `$app-apprequest-prod-abc123`)
   - Copy the **Password**

2. **Add app settings** in Azure Portal:
   - Go to your App Service → **Configuration** → **Application settings**
   - Add these settings:

   | Name | Value |
   |------|-------|
   | `Deployment__PublishUser` | Your FTPS username (e.g., `$app-apprequest-prod-abc123`) |
   | `Deployment__PublishPassword` | Your FTPS password |

3. **Using the update feature**:
   - Go to **Admin** > **Settings** > **Version and Updates**
   - Select **Check for Updates** to see if a new version is available
   - If configured correctly, an **Install Update** button appears
   - Select it to download and deploy the update automatically
   - The application will restart during the update process

> **Note**: The Install Update button only appears when:
> - The portal is running in Azure App Service (not locally)
> - Deployment credentials are properly configured
> - An update is available

#### Manual updates

If auto-update is not configured, you can manually update using either method below:

**Method 1: Kudu ZIP Deploy (recommended for existing installations)**

For existing deployments, use the Kudu ZIP deployment feature:

1. Go to the [releases repository](https://github.com/powerstacks-corp/app-store-for-intune/releases)
2. Download the latest `AppRequestPortal-X.X.X.zip` file (not the source code)
3. In Azure Portal, go to your App Service
4. Select **Advanced Tools** → **Go** (opens Kudu)
5. Select **Tools** → **Zip Push Deploy**
6. Drag and drop the downloaded ZIP file into the deployment area
7. Wait for deployment to complete (watch the logs)
8. Restart your App Service if needed
9. Database migrations will run automatically on next startup

!!! note
    This method preserves your existing configuration and database. The ZIP contains only application files.

**Method 2: Deploy to Azure button (new installations only)**

For fresh installations on an empty resource group:

1. Go to the [releases repository](https://github.com/powerstacks-corp/app-store-for-intune)
2. Select the **Deploy to Azure** button
3. Select an **empty resource group** or create a new one
4. Configure deployment parameters

!!! warning
    The Deploy to Azure button will fail on resource groups containing existing resources. Use Method 1 for existing deployments.

### License management

The portal requires a valid PowerStacks license to operate. License status is displayed in the Admin Dashboard and affects portal functionality.

#### Viewing license status

1. Go to **Admin** > **Settings** tab
2. The **License** section shows:
   - Current license status (Valid, Expired, Over Device Limit, etc.)
   - License type and expiration date
   - Device count vs. licensed limit
   - Last validation timestamp

#### License validation

The portal automatically validates your license:

- On application startup
- Every 24 hours
- When you manually select **Validate License**

To force a validation check, select the **Validate License** button in the License section.

#### Updating license key

1. Go to **Admin** > **Settings** tab
2. In the **License** section, enter your new license key
3. Select **Save License Key**
4. The portal validates the new key and displays the result

Alternatively, use the **Setup Wizard** to enter or update your license key.

#### License warnings

Users see warning banners in the following situations:

| Condition | Banner Message |
|-----------|----------------|
| License expiring soon (≤30 days) | "License expires in X days. Please contact your IT administrator to renew." |
| Device count in grace period (up to 3% over limit) | "Device count exceeds license limit by X devices. Please contact your IT administrator to upgrade." |
| License invalid/expired | Warning message explaining the issue |

!!! note
    When device count exceeds the license limit by more than 3%, new app requests are blocked until the license is upgraded or device count is reduced.

#### Device count

The portal tracks managed devices from Intune that have checked in within the last 30 days. Device count is updated:

- During each app sync from Intune
- When you select **Update Device Count** in the License section

### Display settings

Configure the portal's visual appearance for all users.

| Setting | Description |
|---------|-------------|
| **Enable dark mode** | Toggle dark mode on/off for all portal users (default setting) |
| **Max featured apps on home page** | Maximum number of featured apps to display in the home page carousel (default: 8) |
| **Hero App** | Select one app to feature prominently at the top of the home page |

**Dark mode behavior:**

The portal supports multiple dark mode sources with the following priority:

1. **User preference** - Users can select the sun/moon icon in the header to toggle dark mode for themselves
2. **System preference** - If the user hasn't set a preference, the portal auto-detects the operating system's dark mode setting
3. **Admin default** - Falls back to the admin-configured dark mode setting

User preferences are stored in localStorage and persist across sessions. Users can always override the admin setting for their own viewing preference.

**Dark mode styling:**

When dark mode is enabled, the portal uses a vignette-style design inspired by Microsoft Learn and Intune admin center:

- **Main content area**: Darkest (#1a1a1a) with subtle inset shadow for depth
- **Header/Footer**: Medium dark (#252525) with subtle borders
- **Outer edges**: Lighter dark gray (#2d2d2d)

This creates a professional look where the center content draws focus while the periphery provides visual framing.

!!! note
    Dark mode settings persist across page refreshes and sign-in/sign-out cycles. The admin setting is loaded via a public API endpoint so it applies even before the user authenticates.

### App deployment settings

| Setting | Description |
|---------|-------------|
| **Group Name Prefix** | Prefix used when auto-creating Entra ID groups (default: `AppStore-`). Groups are named `{prefix}{AppName}-Required`. Use this to identify portal-managed groups in your tenant. |

### Custom domain configuration

The Settings tab includes a **Custom Domain** section for configuring a custom domain (e.g., `apps.yourdomain.com`) for your portal.

#### Prerequisites

Before configuring a custom domain:

1. Your DNS must be configured with the appropriate CNAME or A record pointing to your Azure App Service
2. Your Azure App Service must be on the Basic tier or higher (required for custom domains with SSL)

#### Configuring via Admin Dashboard

1. Go to **Admin** > **Settings** tab
2. Scroll to the **Custom Domain** section
3. Read the prerequisites and ensure DNS is configured
4. Select **Configure Custom Domain in Azure**
5. This opens the Azure Portal with a pre-configured ARM template that:
   - Adds your custom domain to the App Service
   - Creates a free Azure-managed SSL certificate
   - Binds the certificate to your domain

#### After configuration

Once your custom domain is configured:

1. **Update Microsoft Entra ID redirect URIs** - Add your custom domain URLs to your App Registration
2. **Update Portal URL** - In Communications > Email Notifications, update the Portal URL to use your custom domain
3. **Test authentication** - Sign out and sign back in to verify authentication works

!!! note
    For detailed DNS configuration, certificate options, and troubleshooting, see [Custom Domains](custom-domains.md).
