---
title: "PowerShell API examples"
description: "Copy-paste-runnable PowerShell scripts for the most common App Store for Intune API automation scenarios."
---

# PowerShell API examples

Working scripts for the three automation patterns App Store for Intune is most often integrated into:

1. **CI/CD upload of a custom MSI** — your build pipeline pushes a freshly built MSI to App Store and it lands as a published app.
2. **CVE-driven update trigger** — an external CVE feed (Defender, Tenable, Qualys, internal vuln scanner) detects a vulnerable app and tells App Store to check for and deploy updates.
3. **Deployment status monitoring** — pull active deployment state into an observability dashboard or scheduled report.

Every example assumes you've already followed [Authentication](authentication.md) to get a token, and that you have `$accessToken` and `$appStoreHost` set. A reusable token-fetching helper is at the bottom of this page.

## CI/CD upload of a custom MSI

The end-to-end flow for adding a custom in-house MSI to your App Store catalog from a build pipeline. Two calls: `inspect` reads the MSI's Property table and extracts metadata, then `publish` confirms the metadata and pushes the app through the packaging queue.

```powershell
$accessToken = Get-AppStoreToken   # see helper at the bottom of this page
$appStoreHost = 'https://<your-app-store-host>'
$headers = @{ Authorization = "Bearer $accessToken" }
$msiPath = '.\dist\InternalLineOfBusinessApp-2.4.1.msi'

# 1. Inspect the MSI. Server reads the Property table and returns
#    ProductCode, ProductName, ProductVersion, Manufacturer, etc.
$form = @{ file = Get-Item -Path $msiPath }
$inspectResult = Invoke-RestMethod `
    -Method Post `
    -Uri "$appStoreHost/api/admin/app-upload/inspect" `
    -Headers $headers `
    -Form $form

Write-Host "MSI inspected:"
$inspectResult | Format-List

# 2. Publish. Pass the inspected metadata, override any fields the
#    pipeline wants to set explicitly (display name, description, icon).
$publishRequest = @{
    uploadId      = $inspectResult.uploadId
    productName   = $inspectResult.productName
    productVersion = $inspectResult.productVersion
    manufacturer  = $inspectResult.manufacturer
    productCode   = $inspectResult.productCode
    displayName   = 'Internal LOB App'
    description   = 'Released by CI build pipeline.'
} | ConvertTo-Json

$publishResult = Invoke-RestMethod `
    -Method Post `
    -Uri "$appStoreHost/api/admin/app-upload/publish" `
    -Headers ($headers + @{ 'Content-Type' = 'application/json' }) `
    -Body $publishRequest

Write-Host "App queued for packaging. Job ID: $($publishResult.packagingJobId)"
```

Drop this in your build pipeline after the MSI artifact step. The packaging job flows through the same queue WinGet apps use; the app appears in App Management once packaging completes.

## CVE-driven update trigger

When your security tooling flags a vulnerable application version, this script tells App Store to refresh its WinGet update cache, look at what's available, and (if there's an update for the affected app) report it. You can extend it to auto-deploy by calling the deployment endpoints.

```powershell
$accessToken = Get-AppStoreToken
$appStoreHost = 'https://<your-app-store-host>'
$headers = @{ Authorization = "Bearer $accessToken" }

# An example CVE feed item identifying a vulnerable app by WinGet ID.
$vulnerableAppId = '7zip.7zip'   # in practice this comes from your CVE feed

# 1. Force a fresh WinGet cache sync so we see the latest available versions.
Invoke-RestMethod `
    -Method Post `
    -Uri "$appStoreHost/api/winget/cache/trigger-sync" `
    -Headers $headers

# 2. Poll the cache status until the sync completes (typically under a minute).
do {
    Start-Sleep -Seconds 5
    $status = Invoke-RestMethod -Uri "$appStoreHost/api/winget/cache/status" -Headers $headers
    Write-Host "Sync status: $($status.state)"
} while ($status.state -in @('Running', 'Queued'))

# 3. Pull available updates and check whether our vulnerable app has one.
$updates = Invoke-RestMethod -Uri "$appStoreHost/api/winget/updates/available" -Headers $headers
$relevant = $updates | Where-Object { $_.wingetPackageId -eq $vulnerableAppId }

if ($relevant) {
    Write-Host "Update available for $vulnerableAppId : $($relevant.currentVersion) -> $($relevant.latestVersion)"
    # Wire in your deployment trigger here, for example:
    # Invoke-RestMethod -Method Post -Uri "$appStoreHost/api/admin/update-deployments" -Headers $headers -Body (@{ appId = $relevant.appId } | ConvertTo-Json) -ContentType 'application/json'
} else {
    Write-Host "No update available for $vulnerableAppId at this time."
}
```

Schedule this hourly from your CVE pipeline or trigger it from a webhook on each new CVE notification.

## Deployment status monitoring

Pull the active update deployments and their status into a CSV your monitoring system can ingest.

```powershell
$accessToken = Get-AppStoreToken
$appStoreHost = 'https://<your-app-store-host>'
$headers = @{ Authorization = "Bearer $accessToken" }

$deployments = Invoke-RestMethod `
    -Uri "$appStoreHost/api/admin/update-deployments" `
    -Headers $headers

$deployments |
    Select-Object id, appName, fromVersion, toVersion, status, currentRing, ringsCompleted, startedAt, completedAt |
    Export-Csv -Path '.\app-store-deployments.csv' -NoTypeInformation

Write-Host "$(($deployments).Count) deployment(s) exported."
```

Run this from your monitoring system on a 5-minute cadence and feed the CSV into whatever dashboarding tool the team uses, or pull each deployment's detail at `/api/admin/update-deployments/{id}` when you want to drill in.

## Reusable token helper

A small helper function the examples above assume is in scope. Drop it in your script library or module.

```powershell
function Get-AppStoreToken {
    [CmdletBinding()]
    param(
        [string]$TenantId     = $env:APPSTORE_TENANT_ID,
        [string]$ClientId     = $env:APPSTORE_CLIENT_ID,
        [string]$ClientSecret = $env:APPSTORE_CLIENT_SECRET,
        [string]$ApiScope     = $env:APPSTORE_API_SCOPE
    )

    $response = Invoke-RestMethod `
        -Method Post `
        -Uri "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token" `
        -Body @{
            client_id     = $ClientId
            client_secret = $ClientSecret
            scope         = $ApiScope
            grant_type    = 'client_credentials'
        }

    return $response.access_token
}
```

Set the four environment variables once in your CI runner (or in your local profile for ad-hoc use), and every example above just works without further config.

## What's next

- The full endpoint catalog (request bodies, response shapes, error codes) is in the OpenAPI spec at `https://<your-app-store-host>/swagger`. See the [API reference overview](index.md) for the link.
- BI for Intune via Power BI is the right place for reporting data export (XMLA endpoint, Power BI REST API, dataflows). See the [BI for Intune docs](https://docs.powerstacks.com/bi-for-intune/) for those patterns.
