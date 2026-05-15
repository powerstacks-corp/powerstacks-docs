---
title: "Create Entra app registrations"
description: "Create the backend and frontend Entra ID app registrations and record the values you'll supply to the Deploy to Azure wizard."
---

# Create Entra app registrations

App Store for Intune uses two app registrations in your tenant:

- The **backend** validates the user tokens that arrive on every `/api/*` call and exposes the `access_as_user` scope that the frontend asks the user to consent to.
- The **frontend** handles user sign-in in the browser and requests the backend's `access_as_user` scope.

Microsoft Graph application permissions live on the App Service's managed identity, not on either app registration. You assign those permissions to the managed identity after the deploy completes by running a single PowerShell snippet — see [Grant Microsoft Graph permissions to the App Service](grant-graph-permissions.md). The app registrations themselves carry no client secret and no Graph application permissions.

## Backend app registration

1. Navigate to **Azure Portal** > **Microsoft Entra ID** > **App registrations**.
2. Select **New registration**.
3. **Name**: `App Store for Intune - Backend`.
4. **Supported account types**: **Single tenant only**.
5. **Redirect URI**: leave empty.
6. Select **Register**.
7. Record the **Application (client) ID** — you'll supply this to the Deploy to Azure wizard.

8. Expose an API scope so the frontend can call the backend on behalf of the signed-in user:
    - Select **Expose an API** > **Add a scope**.
    - **Application ID URI**: accept the default (`api://<client-id>`).
    - Select **Save and continue**.
    - **Scope name**: `access_as_user`
    - **Who can consent**: **Admins and users**
    - **Admin consent display name**: `Access App Store for Intune`
    - **Admin consent description**: `Allows the app to access the App Store for Intune backend as the signed-in user.`
    - **User consent display name**: `Access App Store for Intune`
    - **User consent description**: `Allows the app to access the App Store for Intune backend on your behalf.`
    - **State**: **Enabled**
    - Select **Add scope**.

## Frontend app registration

1. Navigate to **Azure Portal** > **Microsoft Entra ID** > **App registrations**.
2. Select **New registration**.
3. **Name**: `App Store for Intune - Frontend`.
4. **Supported account types**: **Single tenant only**.
5. **Redirect URI**: leave empty for now. After the deploy completes you'll add the App Service URL — see [Add the production redirect URI](add-redirect-uri.md).
6. Select **Register**.
7. Record the **Application (client) ID** — you'll supply this to the Deploy to Azure wizard.

8. Configure API permissions:
    - Select **API permissions** > **Add a permission**.
    - Select **APIs my organization uses** > select your backend app registration.
    - Check `access_as_user`.
    - Select **Add permissions**.
    - Select **Add a permission** again.
    - Select **Microsoft Graph** > **Delegated permissions** > `User.Read`. This permission reads the signed-in user's profile and is used to display the profile photo in the portal header.
    - Select **Add permissions**.
    - Select **Grant admin consent**.

## Next step

Continue to [Deploy to Azure](deploy-to-azure.md).
