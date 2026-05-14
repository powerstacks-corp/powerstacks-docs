---
title: "Create Entra App Registrations"
description: "Create the backend API and frontend SPA app registrations in Microsoft Entra ID, grant Graph permissions, and capture the client IDs and secret."
---

# Create Entra App Registrations

You need to create two app registrations in Entra ID.

## Backend API app registration

1. Navigate to Azure Portal > Microsoft Entra ID > App registrations
2. Click "New registration"
3. Name: `App Store for Intune - API`
4. Supported account types: "Accounts in this organizational directory only"
5. Redirect URI: Leave empty for now
6. Click "Register"

7. Note the **Application (client) ID** and **Directory (tenant) ID**

8. Configure API permissions:
   - Click "API permissions" > "Add a permission"
   - Select "Microsoft Graph" > "Application permissions"
   - Add the following permissions:
     - `DeviceManagementApps.Read.All` - Read Intune apps
     - `DeviceManagementApps.ReadWrite.All` - Manage Intune apps and create assignments
     - `DeviceManagementConfiguration.Read.All` - Read Intune assignment filters (used by ring deployment settings)
     - `DeviceManagementManagedDevices.Read.All` - Read user devices
     - `Group.ReadWrite.All` - Create and manage security groups
     - `User.Read.All` - Read user profiles, managers, and group memberships
     - `Directory.Read.All` - Read directory data
     - `Mail.Send` - Send email notifications (optional, see [Configure Email Notifications](configure-email-notifications.md))
   - Click "Grant admin consent"

   > **Note:** `DeviceManagementApps.ReadWrite.All` is required to automatically create Intune app assignments when apps are made visible in the portal.
   >
   > **Note:** `DeviceManagementConfiguration.Read.All` is required for the Intune assignment-filter picker used in ring deployment settings (per-ring filters and per-app filters). Without this permission the filter dropdown will be empty even if your tenant has filters configured.

9. Create a client secret:
   - Click "Certificates & secrets" > "New client secret"
   - Description: `API Secret`
   - Expires: Choose appropriate duration
   - Click "Add"
   - **Copy the secret value immediately** (you won't be able to see it again)

10. Expose an API:
    - Click "Expose an API" > "Add a scope"
    - Application ID URI: Accept default or use `api://your-api-client-id`
    - Scope name: `access_as_user`
    - Who can consent: Admins and users
    - Display name: `Access API as user`
    - Description: `Allow the application to access the API as the signed-in user`
    - Click "Add scope"

## Frontend SPA app registration

1. Click "New registration"
2. Name: `App Store for Intune - Frontend`
3. Supported account types: "Accounts in this organizational directory only"
4. Redirect URI:
   - Type: "Single-page application (SPA)"
   - URI: `http://localhost:3000`
5. Click "Register"

6. Note the **Application (client) ID**

7. Configure API permissions:
   - Click "API permissions" > "Add a permission"
   - Select "APIs my organization uses" > Select your backend API app
   - Check `access_as_user`
   - Click "Add permissions"
   - Also add "Microsoft Graph" > "Delegated permissions" > `User.Read` (used for profile photo)
   - Click "Grant admin consent"

8. Configure authentication:
   - Click "Authentication"
   - Settings
   - Under "Implicit grant and hybrid flows", check:
     - Access tokens
     - ID tokens
   - Click "Save"

## Next step

Continue to [Configure Application Settings](configure-application-settings.md).
