---
title: "Add the production redirect URI"
description: "Add the App Service URL to the frontend app registration's Single-page application platform so users can sign in."
---

# Add the production redirect URI

Before anyone can sign in to the portal, the frontend app registration needs to know which URL the user will be redirected to after authentication. The App Service URL is generated during deploy and is shown in the deployment outputs.

## Find the App Service URL

The deploy output includes the App Service URL. To retrieve it:

1. Go to **Azure Portal** > your resource group > **Deployments**.
2. Select the deployment that just completed.
3. Select **Outputs** in the left navigation.
4. Copy the value of **appUrl**. It looks like `https://<sitename>.azurewebsites.net`.

You can also retrieve it later from **App Service** > **Overview** > **Default domain**.

## Add the redirect URI

1. Go to **Azure Portal** > **Microsoft Entra ID** > **App registrations**.
2. Select your frontend app registration.
3. Select **Authentication**.
4. Select **Add a platform** > **Single-page application**.
5. Enter the App Service URL with a trailing slash, for example:

    ```text
    https://<sitename>.azurewebsites.net/
    ```

6. Select **Configure**.

## Using a custom domain

If you plan to access the portal through a custom domain, configure the custom domain first by following [Custom Domains](../../administration/custom-domains.md), then add the custom domain URL as the redirect URI in place of (or in addition to) the App Service URL.

## Next step

Continue to [Sign in and verify](sign-in.md).
