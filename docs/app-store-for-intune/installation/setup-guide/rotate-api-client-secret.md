---
title: "Rotate the API client secret"
description: "How to issue a new client secret on the backend API app registration and update Key Vault so the portal picks it up without redeploying."
---

# Rotate the API client secret

The backend API app registration uses a client secret to call Microsoft Graph. That secret has an expiration date you chose when you created it. When it expires, the portal stops being able to call Graph: Intune syncs fail, new apps can't be deployed, and the Teams bot returns 401 on `/api/messages`.

Rotate the secret on or before the expiration date. The rotation is a five-minute operation, and the portal does not need to be redeployed. The new secret value is written to Key Vault; the App Service picks it up automatically on the next restart.

!!! tip "Plan ahead"
    When you create the secret in the [Backend API app registration](create-entra-app-registrations.md#backend-api-app-registration) step, the longest expiration Entra lets you set is 24 months. Put a calendar reminder one month before the expiration so you have a clean rotation window.

## Issue a new client secret

1. Navigate to **Azure Portal** > **Microsoft Entra ID** > **App registrations**
2. Select the backend API app registration (the one named `App Store for Intune - API` or whatever you called it).
3. Click **Certificates & secrets** > **Client secrets** > **New client secret**.
4. Description: something that distinguishes it from the previous secret, e.g., `API Secret 2028`.
5. Expires: pick a new expiration that matches your rotation policy.
6. Click **Add**.
7. **Copy the secret value immediately** — Azure shows it once and only once.

Leave the old secret in place for now. You'll remove it after the new secret is confirmed working.

## Update the Key Vault secret

The deploy template wrote the API client secret to Key Vault as a secret named `AzureAdClientSecret`. Update that secret with the new value.

1. Navigate to **Azure Portal** > **Key vaults** > select the vault the deploy template provisioned (it's in the same resource group as your App Service, with a name like `<sitename>-kv`).
2. Click **Secrets** > select `AzureAdClientSecret`.
3. Click **+ New Version**.
4. Paste the new secret value into the **Secret value** field.
5. Leave the activation/expiration dates empty unless your organization requires them.
6. Click **Create**.

The new version becomes the current version. The App Service's `@Microsoft.KeyVault(SecretUri=...)` reference resolves to whatever version is current, so no further configuration change is needed.

## Restart the App Service

The App Service caches Key Vault references. To force it to read the new version:

1. Navigate to **Azure Portal** > **App Services** > select your App Store App Service.
2. Click **Restart** at the top of the **Overview** blade.
3. Wait two to three minutes for the cold start.

## Verify the new secret is in use

1. Sign in to the portal as an admin.
2. Open `https://<your-app-service-url>/health` — should return `200 OK`.
3. Trigger a Graph-backed action that requires the secret to work — for example, **Admin** > **App Catalog** > click **Sync from Intune**. If it returns results, the new secret is in use. If it returns 401 from Graph, the secret didn't update — recheck the Key Vault value and restart again.

## Delete the old secret

After you've confirmed the portal is healthy on the new secret:

1. Return to the backend API app registration's **Certificates & secrets** blade.
2. Find the previous secret and click the trash icon to delete it.

Leaving the old secret in place doesn't break anything — Entra accepts any non-expired secret on the app registration — but cleaning it up removes a stale credential from your tenant.

## When the rotation fails

- **Graph calls return 401 after restart** — Key Vault still has the old value, or you pasted the wrong value into the new version. Open the secret in Key Vault, click the latest version, and check the **Secret value** with **Show secret value**. Compare against what you copied from the app registration.
- **App Service restart didn't pick up the new value** — try **Stop** then **Start** instead of **Restart**. The standard restart sometimes keeps cached Key Vault references warm.
- **You lost the secret value before storing it in Key Vault** — issue another secret and discard the lost one. Secrets are write-once-read-never by design; there is no recovery path for a lost value.

## Future direction

The product roadmap includes moving the Graph auth flow off client secrets entirely in favor of the App Service's system-assigned managed identity. Once that ships, this rotation procedure goes away — there will be no secret to rotate. Until then, this is the current process.

## Related

- [Create Entra App Registrations](create-entra-app-registrations.md) — original secret creation
- [Deploy to Azure](deploy-to-azure.md) — install flow that stores the secret in Key Vault
- [Security Overview](../../administration/security.md) — overall security model
