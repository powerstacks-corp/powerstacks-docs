---
title: "Grant Microsoft Graph permissions to the App Service"
description: "Run a one-time PowerShell snippet that assigns the required Microsoft Graph application roles to the App Service's managed identity."
---

# Grant Microsoft Graph permissions to the App Service

The App Service authenticates to Microsoft Graph using its system-assigned managed identity. Azure Portal does not have a UI for assigning Microsoft Graph application permissions to a managed identity, so this step is a single PowerShell snippet you run once against Microsoft Graph PowerShell. After it completes, the App Service can call Graph as itself — no client secret, no stored credential.

!!! tip "Wait 10 to 15 minutes after the deploy reports success"
    The App Service's system-assigned managed identity takes 10 to 15 minutes to propagate across Microsoft Entra ID. Run this snippet only after that window has elapsed. Running it earlier returns a "service principal not found" error.

## Find the App Service principal ID

The deploy output includes the App Service's managed identity principal ID. To retrieve it:

1. Go to **Azure Portal** > your resource group > **Deployments**.
2. Select the deployment that just completed.
3. Select **Outputs** in the left navigation.
4. Copy the value of **appServicePrincipalId**.

You can also retrieve it later from **App Service** > **Identity** > **System assigned** > **Object (principal) ID**.

## Run the snippet

Open a PowerShell session with the [Microsoft Graph PowerShell SDK](https://learn.microsoft.com/powershell/microsoftgraph/installation) installed (`Install-Module Microsoft.Graph -Scope CurrentUser`), or use [Azure Cloud Shell](https://shell.azure.com), which has the module pre-installed.

Paste the principal ID into the first line, then run the rest:

```powershell
# Paste the appServicePrincipalId from the deploy output
$AppServicePrincipalId = "<paste-the-principal-id-from-deploy-output>"

Connect-MgGraph -Scopes "AppRoleAssignment.ReadWrite.All","Application.Read.All"

# Verify the App Service's managed identity has propagated to Microsoft Entra ID
# before attempting to grant permissions. If this check fails, the propagation
# window has not yet elapsed.
$AppSp = Get-MgServicePrincipal -ServicePrincipalId $AppServicePrincipalId -ErrorAction SilentlyContinue
if (-not $AppSp) {
    Write-Warning "App Service principal $AppServicePrincipalId not found in Microsoft Entra ID. Please wait a few minutes for the App Service's system-assigned managed identity to propagate across Microsoft Entra ID, then try again."
    return
}

$GraphSp = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"

$Permissions = @(
    "DeviceManagementApps.Read.All",
    "DeviceManagementApps.ReadWrite.All",
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementManagedDevices.Read.All",
    "Group.ReadWrite.All",
    "User.Read.All",
    "Mail.Send"
)

foreach ($p in $Permissions) {
    $role = $GraphSp.AppRoles | Where-Object { $_.Value -eq $p }
    if (-not $role) {
        Write-Warning "App role $p not found on Microsoft Graph. Skipping."
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

The snippet takes about 10 seconds.

## What each permission is for

| Permission | Used for |
| ---------- | -------- |
| `DeviceManagementApps.Read.All` | Read the existing Intune app catalog and assignment state |
| `DeviceManagementApps.ReadWrite.All` | Create and update Intune Win32 app deployments |
| `DeviceManagementConfiguration.Read.All` | Read Intune assignment filters used by ring deployment settings |
| `DeviceManagementManagedDevices.Read.All` | Read managed devices associated with the requesting user |
| `Group.ReadWrite.All` | Create and manage the security groups that drive app assignments |
| `User.Read.All` | Read user profiles, managers, and group memberships for approvals |
| `Mail.Send` | Send email notifications from a configured mailbox (optional, used only if email notifications are enabled) |

## Verify the grant

In Azure Portal, go to **Microsoft Entra ID** > **Enterprise applications** > **All applications**. Change the **Application type** filter to **Managed Identities** and find the App Service by name. Select it, then select **Permissions** in the left navigation. You should see all seven Graph application permissions listed with admin consent granted.

You can also verify by signing in to the portal and selecting **Admin** > **App Catalog** > **Sync from Intune**. If apps appear, the permissions are in place.

!!! note "Rerunning the snippet is safe"
    The snippet uses `ErrorAction SilentlyContinue` so re-running after a partial failure, or after a future release adds a permission, is idempotent. Already-granted roles are skipped, missing roles are added.

## Next step

Continue to [Add the production redirect URI](add-redirect-uri.md).
