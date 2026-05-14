---
title: "Configure Admin Access"
description: "Required step. Create the admin security group and set AdminGroupId before anyone can use admin features. Without it, all admin endpoints return 403."
---

# Configure Admin Access

> **CRITICAL (v1.10.6+):** You **must** configure the `AdminGroupId` before anyone can access admin functions. The portal uses a fail-closed security model. If no admin group is configured, **all admin endpoints return 403 Forbidden** for every user, including the person who deployed the portal. There is no first-run setup wizard. If you skip this step, the only way to recover admin access is to set the `AdminGroupId` in `appsettings.json` or the `AppSettings__AdminGroupId` environment variable and restart the application.

## Create security groups

1. Navigate to Azure Portal > Microsoft Entra ID > Groups
2. Create a new security group:
   - Group type: **Security**
   - Group name: `AppStore-Admins` (or your preferred name)
   - Group description: `Administrators for the App Store for Intune`
   - Membership type: **Assigned**
3. Click **Create**
4. Add users who should have admin access to this group
5. Copy the **Object ID** of the group (found on the group's Overview page)

## Set AdminGroupId in configuration (required)

You **must** set `AdminGroupId` before the first admin can log in. Choose one of the following methods:

**Method 1: appsettings.json**. Update `appsettings.json`:

```json
{
  "AppSettings": {
    "AdminGroupId": "your-admin-group-object-id",
    "ApproverGroupId": "your-approver-group-object-id"
  }
}
```

**Method 2: Environment variable** (recommended for Azure App Service):

```
AppSettings__AdminGroupId=your-admin-group-object-id
AppSettings__ApproverGroupId=your-approver-group-object-id
```

**Configuration options:**

| Setting | Description |
|---------|-------------|
| `AdminGroupId` | **(Required)** Object ID of the Entra ID group for administrators. Admins can sync apps from Intune and manage all settings. **Without this, no user can access admin features.** |
| `ApproverGroupId` | Object ID of the Entra ID group for approvers. Approvers can approve/reject app requests. |

You can use the same group for both settings, or create separate groups for more granular control.

## Configure additional settings via portal UI

Once you have initial admin access (via the configuration above):

1. Navigate to **Admin** > **Settings** tab
2. Under **Group-Based Authorization**:
   - Enter the **Admin Group** Object ID (this saves it to the database so it persists independently of `appsettings.json`)
   - Enter the **Approver Group** Object ID
3. Under **App Deployment Settings**:
   - Set the **Group Name Prefix** (default: `AppStore-`). This prefix is used when auto-creating Entra ID security groups for app deployments
4. Click **Save Settings**

See the [Admin Guide](../../administration/) for detailed instructions on using the Portal Settings UI.

> **Note:** The portal checks the database settings first, then falls back to `appsettings.json`. Once you configure the admin group via the UI, the `appsettings.json` value is a fallback only. Keep the `appsettings.json` value as a recovery mechanism in case the database value is accidentally cleared.

## App deployment settings

The portal automatically creates Entra ID security groups and Intune app assignments when apps are made visible. Configure the group naming:

| Setting | Default | Description |
|---------|---------|-------------|
| `GroupNamePrefix` | `AppStore-` | Prefix for auto-created security groups. Groups are named `{prefix}{AppName}-Required`. |

This setting is configured via the Portal Settings UI (Admin > Settings > App Deployment Settings).

> **Tip:** Settings configured in the UI take precedence over appsettings.json values. The initial values from appsettings.json seed the database on first run.

## Next step

Continue to [Deploy to Azure](deploy-to-azure.md).
