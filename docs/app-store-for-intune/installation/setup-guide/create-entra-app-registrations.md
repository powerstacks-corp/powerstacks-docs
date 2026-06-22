---
title: "Create the Entra app registration"
description: "Create the single Entra ID app registration App Store for Intune uses for sign-in and incoming-token validation, and record the values you'll supply to the Deploy to Azure wizard."
---

# Create the Entra app registration

App Store for Intune uses **one** app registration in your tenant. It plays two roles, both bound to the same client ID:

- **Sign-in** — the portal's sign-in page redirects users here, then receives an access token scoped to `access_as_user`.
- **Token validation** — the backend API trusts only tokens whose audience matches this client ID, then checks the scope.

A single app registration can do both: expose the `access_as_user` scope (the audience) and configure a Single-page application platform with redirect URIs (the sign-in surface).

!!! note "Why the app registration looks 'empty'"
    The only delegated permission this app uses is `User.Read`, which is added by default when you register the app (it renders the signed-in user's profile photo in the portal header). There is **no client secret**, and there are **no Microsoft Graph application permissions** on the app registration itself.

    That's intentional. Microsoft Graph application permissions live on the App Service's system-assigned managed identity, not on the app registration. You grant those permissions to the managed identity after deploy by running a single PowerShell snippet — see [Grant Microsoft Graph permissions to the App Service](grant-graph-permissions.md). If a reviewer looks at the App Store app registration and asks "where are the Graph permissions?", the answer is "on the App Service's managed identity, by design."

## Register the application

1. Go to **Azure Portal** > **Microsoft Entra ID** > **App registrations**.
2. Select **New registration**.
3. **Name**: `App Store for Intune`.
4. **Supported account types**: **Single tenant only**.
5. **Redirect URI**: leave empty for now. After the deploy completes you'll add the App Service URL — see [Add the production redirect URI](add-redirect-uri.md).
6. Select **Register**.
7. Record the **Application (client) ID** — you'll supply this to the Deploy to Azure wizard. This is the only value you need from the app registration: the tenant ID is detected automatically during deployment, and there's no client secret and no second app registration.

## Expose the `access_as_user` scope

This is what the backend uses to validate incoming tokens, and what the portal asks the user to consent to during sign-in.

1. Select **Expose an API** > **Add a scope**.
2. **Application ID URI**: accept the default (`api://<client-id>`).
3. Select **Save and continue**.
4. **Scope name**: `access_as_user`
5. **Who can consent**: **Admins and users**
6. **Admin consent display name**: `Access App Store for Intune`
7. **Admin consent description**: `Allows the app to access the App Store for Intune backend as the signed-in user.`
8. **User consent display name**: `Access App Store for Intune`
9. **User consent description**: `Allows the app to access the App Store for Intune backend on your behalf.`
10. **State**: **Enabled**
11. Select **Add scope**.

## Next step

Continue to [Deploy to Azure](deploy-to-azure.md).
