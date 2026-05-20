---
title: "API authentication"
description: "How to register an Entra app, grant it API access, and request a JWT bearer token for App Store for Intune."
---

# API authentication

App Store for Intune uses **JWT bearer tokens** issued by your Entra ID tenant. Every API request must include `Authorization: Bearer <token>`. Tokens are validated against the App Store backend's Entra app registration: tenant, audience, and signing keys all have to match.

For interactive use you can borrow a token from your own browser session against the running portal (open the network inspector, find an authenticated API request, copy the `Authorization` header). For real automation you'll want a dedicated Entra app registration with permission to call the API.

The rest of this page walks through the dedicated-app-registration path.

## Prerequisites

- Global Administrator or Application Administrator role on the Entra tenant where App Store is deployed (you need this to register apps and grant API permissions).
- App Store for Intune already deployed and accessible in that tenant.
- A note of the App Store API's **Application (client) ID** and **Application ID URI**. Your App Store admin set these during installation; they're in the backend `appsettings.json` under `AzureAd:ClientId` and `AzureAd:Audience`. If you don't have them, see [Create Entra App Registrations](../installation/setup-guide/create-entra-app-registrations.md) for where they came from.

## Register the calling app

1. Sign in to the [Entra admin center](https://entra.microsoft.com).
2. Go to **Identity** → **Applications** → **App registrations** → **+ New registration**.
3. Pick a name that describes the caller (for example, `App Store Automation - CI/CD` or `App Store Automation - CVE Monitor`).
4. Account type: **Accounts in this organizational directory only**.
5. Leave the redirect URI blank. Client credentials grant doesn't use one.
6. Select **Register**.
7. On the new app's overview page, note the **Application (client) ID** and **Directory (tenant) ID**. You'll need both.

## Create a client secret

1. On the new app, go to **Certificates & secrets** → **+ New client secret**.
2. Give it a description and an expiration (24 months is a reasonable default).
3. Select **Add**.
4. **Copy the secret value immediately.** Entra only displays it once. If you miss it, generate a new one.

Store the secret in a real secrets manager (Azure Key Vault, GitHub Actions encrypted secrets, Azure DevOps variable groups, your CI runner's secret store). Never commit it to source control.

## Grant the calling app permission to the App Store API

1. Still on the calling app's registration, go to **API permissions** → **+ Add a permission**.
2. Choose the **APIs my organization uses** tab.
3. Search for your App Store API by the name your administrator used when registering it (default: `App Store for Intune - API`).
4. Pick **Application permissions** (not Delegated), select the role exposed by the API (`Api.Access` or similar; your administrator can confirm the role name), and select **Add permissions**.
5. Back on the API permissions page, select **Grant admin consent for `<tenant name>`**. The status will flip to green when consent is granted.

## Request a token

With the tenant ID, client ID, and client secret from steps 1-2, plus the API's Application ID URI from prerequisites, your caller can request a JWT against Entra's token endpoint:

```powershell
$tenantId   = '<your-tenant-id>'
$clientId   = '<calling-app-client-id>'
$clientSecret = '<calling-app-client-secret>'
$apiScope   = 'api://<app-store-application-id-uri>/.default'

$tokenResponse = Invoke-RestMethod `
    -Method Post `
    -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" `
    -Body @{
        client_id     = $clientId
        client_secret = $clientSecret
        scope         = $apiScope
        grant_type    = 'client_credentials'
    }

$accessToken = $tokenResponse.access_token
```

The returned `access_token` is a JWT valid for one hour (configurable in Entra). Cache it in your script and re-request when it expires.

## Call the API

```powershell
$appStoreHost = 'https://<your-app-store-host>'
$headers = @{ Authorization = "Bearer $accessToken" }

$apps = Invoke-RestMethod -Uri "$appStoreHost/api/Apps" -Headers $headers
$apps | Select-Object id, name, publisher, version | Format-Table
```

That's the round trip. Once you have a token, every endpoint in the [API reference](index.md) is a straight HTTP call.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `401 Unauthorized` immediately | Token wasn't included, or the `Authorization` header is malformed | Confirm the header is `Authorization: Bearer <token>` with a single space |
| `401 Unauthorized` with a token included | Token audience doesn't match the API's expected audience | Verify `scope` in the token request uses the correct Application ID URI; verify the token was issued by the right tenant |
| `403 Forbidden` | Token is valid but the calling app doesn't have the required application permission | Re-check Step 3: API permissions added, role assigned, admin consent granted |
| `429 Too Many Requests` | App Store's per-IP rate limit kicked in | Back off and retry; if the limit is wrong for your use case, raise it in `appsettings.json` `IpRateLimiting:GeneralRules` |
| Token request returns `AADSTS500011` | The API's Application ID URI in the `scope` parameter doesn't exist or is misspelled | Confirm the API URI with your App Store administrator |

## What's next

- **[PowerShell examples](examples.md)** — copy-paste-runnable scripts for the most common automation use cases.
