---
title: "Deploy to Azure"
description: "Run the ARM template deploy. What each parameter is for, what gets provisioned, what to do after deploy completes, and how to troubleshoot the common Key Vault propagation delay."
---

# Deploy to Azure

This is the install. You click the **Deploy to Azure** button, fill the parameter form with the values you collected in the prior steps, and wait 10-15 minutes. The template provisions everything end to end.

## Before you start

You should already have:

- Backend API app registration **client ID** and the **tenant ID** ([Create Entra App Registrations](create-entra-app-registrations.md))
- Frontend SPA app registration **client ID** ([Create Entra App Registrations](create-entra-app-registrations.md))
- Admin security group **Object ID** ([Configure Admin Access](configure-admin-access.md))
- Approver security group **Object ID** ([Configure Admin Access](configure-admin-access.md))

If you don't have all five, go back and finish those pages first. The deploy form will reject empty values.

!!! tip "No client secret in this list"
    Earlier releases required pasting an API client secret into the deploy form. That is gone. The portal authenticates to Microsoft Graph using the App Service's system-assigned managed identity, and the Teams bot uses a user-assigned managed identity that the template provisions for you. No password lives in the install. The post-deploy step below ([Grant Microsoft Graph permissions to the App Service](#grant-microsoft-graph-permissions-to-the-app-service)) is the one piece that still requires a single PowerShell command — a copy-paste snippet that the deploy form prints for you.

## Launch the deploy

Click the **Deploy to Azure** button on the [App Store for Intune GitHub repository](https://github.com/powerstacks-corp/App-Store-for-Intune). Azure Portal opens a custom-deploy form.

!!! note "Azure Marketplace listing"
    A managed Azure Marketplace listing is in the works that will replace the GitHub deploy button as the recommended install path. Until that lands, the button is the install path.

## Fill the parameter form

| Parameter | Where it comes from |
|---|---|
| **Subscription** | The Azure subscription you want App Store installed into. |
| **Resource group** | Create a new resource group, or pick an existing one. Empty is simpler. |
| **Region** | The Azure region for all resources. Pick something close to your users. |
| **Site name** | The App Service name. This becomes `https://<sitename>.azurewebsites.net`. Must be globally unique in Azure. |
| **API client ID** | Backend API app registration's client ID. |
| **Frontend client ID** | Frontend SPA app registration's client ID. |
| **Tenant ID** | Your Entra tenant's directory ID. |
| **Admin group ID** | The Object ID of the admin security group. |
| **Approver group ID** | The Object ID of the approver security group, or the same as admin group if you don't need a split. |
| **SQL admin password** | A new password for the SQL Server admin account. The template generates the SQL Server; this is the password it uses. Save this in your password manager — you may need it for direct database access during troubleshooting. |
| **Enable Teams Bot** | `true` if you want personal Adaptive Card notifications in Teams. The template registers the Azure Bot resource and adds the Teams channel automatically. If `true`, finish [Configure Microsoft Teams Bot](configure-teams-bot.md) after deploy — the Teams app manifest still has to be uploaded in the Teams admin center. |
| **Email settings** | Optional. SMTP details for email notifications. You can leave these blank and configure them via the admin UI after install. |

Click **Review + create**, then **Create**. The deploy takes 10-15 minutes.

## What the template provisions

- **Azure App Service Plan** (B2 tier by default — you can scale up or down post-install) and the **App Service** itself with **system-assigned managed identity** enabled. This identity is the one that calls Microsoft Graph at runtime.
- **A user-assigned managed identity (UAMI)** dedicated to the Teams bot, attached to the App Service alongside the system-assigned MI. The Azure Bot resource is configured with `msaAppType = "UserAssignedMSI"` so its outbound calls to the Bot Connector authenticate without a password.
- **Azure SQL Server** plus the **App Store database**, firewalled to allow only Azure services by default. Database migrations apply automatically on first start, so there is no separate database setup step.
- **Azure Key Vault** containing the SQL connection string and the storage connection string. The App Service's system-assigned managed identity is granted **Get** and **List** permissions on the vault so it can read these at runtime. The vault holds no application secrets — every credential the runtime uses is a managed identity, not a stored value.
- **Azure Storage account** used by the packaging pipeline.
- **Azure Bot** resource and Teams channel registration (if `enableTeamsBot=true`).
- **Application settings** on the App Service, pre-populated with every value the API needs. You do not need to configure anything else in the App Service Configuration blade after deploy.

## After the deploy completes

1. **Wait 10-15 minutes for managed identity propagation.** Even after the deploy reports success, the App Service's managed identity may not yet be readable across Azure AD. See [Key Vault reference failures](#key-vault-reference-failures-red-x-marks) below if you see red X marks on Key Vault references in the Configuration blade.

2. **Grant Microsoft Graph permissions to the App Service managed identity** (see the next section). Until you do this, the portal will sign you in but every Graph-backed operation (Intune sync, app deploy, group creation, etc.) will fail with a 403 from Graph.

3. **Add the production redirect URI to the frontend SPA app registration before anyone tries to sign in.** The App Service URL is one of the outputs shown on the deployment completion page — it looks like `https://<sitename>.azurewebsites.net`. Step-by-step instructions are at [Create Entra App Registrations: What to do after the deploy completes](create-entra-app-registrations.md#what-to-do-after-the-deploy-completes). If you want to use a custom domain instead, set it up per [Custom Domains](../../administration/custom-domains.md) first and use that URL as the redirect URI.

4. **Verify the portal is healthy.** Visit:
    - `https://<sitename>.azurewebsites.net/health` — should return `200 OK`
    - `https://<sitename>.azurewebsites.net/health/migrations` — should return `"pendingCount": 0`

5. **Sign in.** Open the portal in a browser. You'll be redirected to Entra ID sign-in. After signing in as a member of the admin group, you should land on the admin tab. If you get a 403, your account isn't in the admin group or the admin group Object ID supplied at deploy was wrong.

6. **Configure optional features.** Continue to [Configure Email Notifications](configure-email-notifications.md), [Configure Microsoft Teams Bot](configure-teams-bot.md), or [Configure Application Insights](configure-application-insights.md) as needed. None are required for the portal to function.

## Grant Microsoft Graph permissions to the App Service

This is the one piece of the install that the deploy template cannot do for you. The Azure portal does not have a UI for assigning Microsoft Graph application permissions to a managed identity, so you do it once with a short PowerShell snippet that the deploy form printed for you in the **Outputs** tab.

The snippet runs against the **Microsoft Graph PowerShell SDK** under your own admin identity (the same role you used to create the app registrations). It looks up the App Service's managed identity service principal in your tenant, then assigns each Graph application role to it — exactly the same set you declared on the backend API app registration, just attached to the runtime identity instead of an app secret.

### Where to find the principal ID

The deploy emits two outputs you need:

- **`appServicePrincipalId`** — the object (principal) ID of the App Service's system-assigned managed identity. The snippet below references this.
- **`appUrl`** — the App Service URL.

Both are visible on the **Outputs** tab of the deployment in Azure Portal: open your resource group → **Deployments** → the deployment that just completed → **Outputs**.

### Run the snippet

Open a PowerShell session — Azure Cloud Shell or a local install of [Microsoft Graph PowerShell](https://learn.microsoft.com/powershell/microsoftgraph/installation) (`Install-Module Microsoft.Graph -Scope CurrentUser`). Paste the principal ID into the first line, then run the rest:

```powershell
# Paste the appServicePrincipalId from the deploy output here
$AppServicePrincipalId = "<paste-the-principal-id-from-deploy-output>"

Connect-MgGraph -Scopes "AppRoleAssignment.ReadWrite.All","Application.Read.All"

$GraphSp = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"

$Permissions = @(
    "DeviceManagementApps.Read.All",
    "DeviceManagementApps.ReadWrite.All",
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementManagedDevices.Read.All",
    "Group.ReadWrite.All",
    "User.Read.All",
    "Directory.Read.All",
    "Mail.Send"
)

foreach ($p in $Permissions) {
    $role = $GraphSp.AppRoles | Where-Object { $_.Value -eq $p }
    if (-not $role) {
        Write-Warning "App role $p not found on Microsoft Graph"
        continue
    }
    New-MgServicePrincipalAppRoleAssignment `
        -ServicePrincipalId $AppServicePrincipalId `
        -PrincipalId $AppServicePrincipalId `
        -ResourceId $GraphSp.Id `
        -AppRoleId $role.Id `
        -ErrorAction SilentlyContinue
    Write-Host "Granted $p"
}
```

That's it. The script takes about 10 seconds. When it finishes, the App Service can call Graph as itself, using its managed identity. No secret was created, no password is stored anywhere.

### Verify the grant

In Azure Portal, open the App Service > **Identity** > **System assigned** > **Azure role assignments**. Switch the scope to **Microsoft Entra role assignments** (or check **Enterprise applications** > find your App Service by name > **Permissions**). You should see the eight Graph application permissions listed, each with admin consent granted.

You can also test it from the portal once everything else is up: sign in as an admin → **Admin** > **App Catalog** > click **Sync from Intune**. If apps appear, the grant is in place. If you get a 403, re-run the snippet or check the verification step above.

!!! note "Rerunning the snippet is safe"
    The script uses `ErrorAction SilentlyContinue` so re-running it after a partial failure (or after Microsoft adds a new required permission in a future release) is idempotent — already-granted roles are skipped, missing roles are added.

## Troubleshooting

### Key Vault reference failures (red X marks)

After the deploy completes, the App Service's Configuration blade may show red X marks next to Key Vault references, and `/health` may return `503 Service Unavailable`. This is an Azure-AD identity propagation delay, not a configuration error.

**Symptoms**

- App Service Configuration shows red X marks next to Key Vault source settings
- `/health` returns `503 Service Unavailable`
- `/health/migrations` returns an error mentioning `'@microsoft.keyvault'`
- App logs show `ArgumentException` related to connection strings

**Root cause**

When deploying with managed identity and Key Vault for the first time, there is a 5-15 minute delay for the App Service's identity to propagate through Azure AD. During that window the App Service can't resolve Key Vault references.

**Fix**

1. **Wait 10-15 minutes**, then refresh the Configuration page. The red X marks should turn green.
2. **Restart the App Service.** Restart picks up newly-resolvable references.
3. Verify `/health` and `/health/migrations` now return success.

If after 30 minutes the references are still failing, check:

- **Managed Identity** at App Service > **Identity** > **System assigned** — Status should be **On**.
- **Key Vault access policy** — there should be a policy granting the App Service's principal **Get** and **List** secret permissions. If missing, add it manually.
- **Key Vault networking** — either "Allow public access from all networks" or the App Service outbound IPs added to the firewall allowlist.
- **Secret names** — open each Key Vault reference in App Service Configuration and check the URL. The secret name must exactly match the secret in Key Vault (case-sensitive).

### Database migration issues

If `/health/migrations` shows `"pendingCount" > 0` after the wait, migrations didn't auto-apply.

1. Restart the App Service. Migrations run on startup.
2. Wait 2 minutes and check `/health/migrations` again.
3. If still pending, check Application Insights logs for migration errors. Common causes:
    - **SQL firewall** — add the App Service outbound IPs to the SQL Server firewall rules.
    - **Connection timeout** — Azure SQL takes a few minutes to be ready on first deploy. Restart again.
    - **Permission denied** — the SQL user the template configured should have `db_owner`. If it doesn't, the template may have failed partway through; redeploy or open a support ticket.

### Sign-in works but admin tab returns 403

The admin group Object ID supplied at deploy doesn't match the group your account is in, or your account isn't a member. Verify the Object ID in **Entra ID** > **Groups** > select the admin group > **Overview**. If the value is wrong, update `AppSettings__AdminGroupId` in App Service Configuration and restart, or re-deploy with the correct value.

For more deployment troubleshooting, see [Troubleshooting](../../administration/troubleshooting.md).

## Next step

Continue to [Configure Email Notifications](configure-email-notifications.md) (optional), or jump to the [Admin Guide](../../administration/index.md) to start configuring the portal.
