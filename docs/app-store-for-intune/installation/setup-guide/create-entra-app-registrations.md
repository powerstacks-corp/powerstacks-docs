---
title: "Create Entra App Registrations"
description: "Create the backend API and frontend SPA app registrations in Microsoft Entra ID, grant Microsoft Graph permissions, and capture the values you'll paste into the Deploy to Azure form."
---

# Create Entra App Registrations

App Store for Intune needs two app registrations in your tenant:

- The **backend API** — calls Microsoft Graph on behalf of the portal to read your Intune apps and create assignments. Holds the Graph permissions and a client secret.
- The **frontend SPA** — handles user sign-in and calls the backend API. Client ID only.

You create both before clicking **Deploy to Azure**, because the deploy form asks for their client IDs and the API's secret.

## Backend API app registration

1. Navigate to **Azure Portal** > **Microsoft Entra ID** > **App registrations**
2. Click **New registration**
3. Name: `App Store for Intune - API`
4. Supported account types: **Accounts in this organizational directory only**
5. Redirect URI: leave empty
6. Click **Register**
7. Note the **Application (client) ID** and **Directory (tenant) ID** — you'll paste both into the Deploy to Azure form.

8. Configure API permissions:
    - Click **API permissions** > **Add a permission**
    - Select **Microsoft Graph** > **Application permissions**
    - Add the following permissions:
        - `DeviceManagementApps.Read.All` — read Intune apps
        - `DeviceManagementApps.ReadWrite.All` — manage Intune apps and create assignments
        - `DeviceManagementConfiguration.Read.All` — read Intune assignment filters (used by ring deployment settings)
        - `DeviceManagementManagedDevices.Read.All` — read user devices
        - `Group.ReadWrite.All` — create and manage security groups
        - `User.Read.All` — read user profiles, managers, and group memberships
        - `Directory.Read.All` — read directory data
        - `Mail.Send` — send email notifications (optional, see [Configure Email Notifications](configure-email-notifications.md))
    - Click **Grant admin consent**

    !!! note "Why these permissions"
        `DeviceManagementApps.ReadWrite.All` is what lets the portal create Intune app assignments when an app is made visible. `DeviceManagementConfiguration.Read.All` is what populates the assignment-filter picker used by ring deployment settings — without it, the filter dropdown is empty even if your tenant has filters configured.

9. Create a client secret:
    - Click **Certificates & secrets** > **New client secret**
    - Description: `API Secret`
    - Expires: pick an expiration that matches your secret-rotation policy. 24 months is a reasonable default.
    - Click **Add**
    - **Copy the secret value immediately** — you won't be able to see it again.

    !!! tip "Where this secret lives after the install"
        You'll paste this value into the Deploy to Azure form once. The deploy template writes it to Azure Key Vault and the App Service reads it from there at runtime using its system-assigned managed identity. After install, you do not need to keep a copy of the secret value — and you should delete any local copies (Notepad, OneNote, password managers) once the deploy completes. When the secret expires, follow [Rotate the API client secret](rotate-api-client-secret.md) to issue a new one without touching the rest of the install.

10. Expose an API (so the frontend can call the backend on behalf of the signed-in user):
    - Click **Expose an API** > **Add a scope**
    - Application ID URI: accept the default or use `api://your-api-client-id`
    - Scope name: `access_as_user`
    - Who can consent: **Admins and users**
    - Display name: `Access API as user`
    - Description: `Allow the application to access the API as the signed-in user`
    - Click **Add scope**

## Frontend SPA app registration

1. Back at **Azure Portal** > **Microsoft Entra ID** > **App registrations**, click **New registration**
2. Name: `App Store for Intune - Frontend`
3. Supported account types: **Accounts in this organizational directory only**
4. Redirect URI:
    - Type: **Single-page application (SPA)**
    - URI: leave this for now. You'll come back after the deploy completes and add the App Service URL.

5. Click **Register**
6. Note the **Application (client) ID** — you'll paste it into the Deploy to Azure form.

7. Configure API permissions:
    - Click **API permissions** > **Add a permission**
    - Select **APIs my organization uses** > select your backend API app
    - Check `access_as_user`
    - Click **Add permissions**
    - Add **Microsoft Graph** > **Delegated permissions** > `User.Read` (used to fetch the signed-in user's profile photo)
    - Click **Grant admin consent**

    !!! note "Auth flow"
        The frontend uses MSAL.js with the authorization-code flow plus PKCE. You do not need to enable any of the **Implicit grant and hybrid flows** checkboxes (Access tokens, ID tokens) on the **Authentication** blade — those are for the legacy implicit flow. Leave them off.

## What to do after the deploy completes

Once [Deploy to Azure](deploy-to-azure.md) finishes, you must add the App Service URL as the SPA redirect URI **before anyone tries to sign in to the portal**. Sign-in will fail until this is done.

The App Service URL is one of the outputs the Deploy to Azure wizard shows on the deployment completion page. It looks like `https://<sitename>.azurewebsites.net`. You can also find it later under **Azure Portal** > **App Services** > select your App Store App Service > **Overview** > **Default domain**.

To add it:

1. Return to **Microsoft Entra ID** > **App registrations** > select your frontend SPA app registration.
2. Open the **Authentication** blade.
3. Click **Add a platform** > **Single-page application** (or, if a SPA platform already exists, click **Add URI** under it).
4. Enter the App Service URL with a trailing slash, for example:

    ```
    https://appstore-contoso.azurewebsites.net/
    ```

5. Click **Configure** (or **Save**).

If you plan to access the portal via a custom domain instead of the default `*.azurewebsites.net` URL, configure the custom domain first per [Custom Domains](../../administration/custom-domains.md), then add the custom domain URL as the SPA redirect URI instead of (or in addition to) the App Service URL.

If you build the portal from source for local development, you can keep `http://localhost:3000` as an additional redirect URI on the same app registration. Production and dev URIs coexist.

## Next step

Continue to [Configure Admin Access](configure-admin-access.md) — create the admin and approver security groups before you deploy, because their Object IDs go into the deploy form.
