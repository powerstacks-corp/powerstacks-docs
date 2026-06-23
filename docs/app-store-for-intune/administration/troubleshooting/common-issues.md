---
title: "Common issues"
description: "Fixes for common App Store for Intune problems: the 403 admin error, WinGet publishing errors, install-status issues, an empty assignment-filter dropdown, and migrations."
---

# Common issues

### All admin pages return 403 Forbidden

**Cause (v1.10.6+):** The portal requires `AdminGroupId` to be configured. If no Admin Group ID is set in either portal settings (database) or `appsettings.json` / environment variables, all admin endpoints return 403 Forbidden.

**Fix:**

1. Set the `AdminGroupId` via environment variable and restart:
   - **Azure App Service:** Go to Configuration → Application Settings → Add `AppSettings__AdminGroupId` with the Microsoft Entra ID group Object ID → Save → Restart
   - **Local/IIS:** Set `AppSettings__AdminGroupId` environment variable, or add to `appsettings.json`:
     ```json
     { "AppSettings": { "AdminGroupId": "your-group-object-id" } }
     ```
2. Restart the application
3. Sign in with an account that is a member of that group
4. Go to Admin → Settings and save the Admin Group ID in portal settings

**Prevention:** Always keep `AdminGroupId` set in `appsettings.json` or environment variables as a fallback, even after configuring it in the portal UI.

### Group or user search in the Setup Wizard is empty

**Symptom:** In the Setup Wizard, searching for a security group (admin group step) or a user (email notification step) returns no results, even though the groups and users exist.

**Cause:** The App Service is using a Microsoft Graph token that was issued *before* the Graph permissions were granted to its managed identity. Graph app-role grants don't apply to a token the app already cached, so directory search stays empty until the App Service gets a fresh token.

**Fix:** Restart the App Service so it requests a new managed-identity token that carries the granted roles: Azure Portal → your App Service → **Restart**. Give the role assignments a couple of minutes to propagate first; if search is still empty immediately after a restart, wait a few minutes and restart once more.

The [Grant Microsoft Graph permissions](../../installation/setup-guide/grant-graph-permissions.md) snippet now performs this wait-and-restart automatically, so this mainly affects installs where the permissions were granted by hand or topped up later.

### WinGet package publishing errors

#### Error: "Failed to download installer manifest from GitHub: NotFound"

**Cause:** Package doesn't exist in Microsoft's winget-pkgs repository, or the path structure is different.

**Diagnosis:**
1. Check Application Insights for the full error message:
   ```kusto
   traces
   | where message contains "Failed to download installer manifest"
   | order by timestamp desc
   | take 10
   ```

2. Look for the manifest URL in the error message
3. Try opening the URL in a browser to verify if it exists

**Solution:**
- Verify the package ID is correct
- Check if the package exists in https://github.com/microsoft/winget-pkgs
- Some packages may not be available in the Microsoft repository
- Try searching for the package at https://winget.run

---

#### Error: 404 when packaging WinGet apps with nested package IDs

**Cause (fixed in v1.11.31):** Some WinGet packages use numeric sub-directories that are part of the package ID rather than version numbers. For example, `Microsoft.SQLServerManagementStudio` has a sub-directory `22/` which is part of the full package ID `Microsoft.SQLServerManagementStudio.22`. Prior to v1.11.31, the system mistakenly treated `22/` as a version directory, then failed to find the manifest file because the actual filename includes the full package ID (e.g., `Microsoft.SQLServerManagementStudio.22.installer.yaml` rather than `Microsoft.SQLServerManagementStudio.installer.yaml`).

**Symptoms:**
- Packaging job fails during the "Downloading" phase
- Application Insights shows a 404 error when fetching the `.installer.yaml` file
- Affected packages include any with numeric sub-directories in the WinGet repo (e.g., `Microsoft.SQLServerManagementStudio`, `Microsoft.DirectX`)

**Solution:** Upgrade to v1.11.31 or later. The fix adds two layers of detection:
1. **Version resolution**: When a numeric directory has no manifest files, the system recognizes it as a package ID segment and drills into the actual version sub-directories
2. **Manifest filename discovery**: If the expected manifest filename returns a 404, the system lists the version directory via the GitHub API to find the correct `.installer.yaml` filename

---

#### Error: "File {filename}.exe can not be found"

**Cause:** Downloaded installer file is missing or failed to download.

**Diagnosis:**
1. Check Application Insights for download logs:
   ```kusto
   traces
   | where message contains "Downloading to:"
   | order by timestamp desc
   | take 20
   ```

2. Look for:
   - "Download complete: {FilePath} ({Size} bytes)" - file downloaded successfully
   - "File verified: {FilePath} exists" - file validation passed
   - Any errors between these log entries

**Possible causes:**
- Download failed (network issue, installer URL invalid)
- File was downloaded but is 0 bytes
- Path or filename too long (Windows 260 character limit)
- Temporary directory cleanup happened before packaging

**Solution:**
- Check the packaging job status for more details
- Verify the installer URL is valid and accessible
- Try publishing the package again
- Check App Service disk space

---

#### Error: "Failed to create .intunewin package"

**Cause:** SvRooij.ContentPrep library couldn't create the .intunewin file.

**Diagnosis:**
1. Check Application Insights for packaging logs:
   ```kusto
   traces
   | where message contains "Creating .intunewin package"
   | order by timestamp desc
   | take 20
   ```

2. Look for the error message from the packager

**Common causes:**
- Installer file doesn't exist (see previous section)
- Installer file is corrupted or 0 bytes
- Insufficient disk space
- Invalid file format

**Solution:**
- Verify the installer downloaded successfully
- Check App Service disk space and scaling
- Try a different package to isolate the issue

---

### Install status issues

#### Install status stuck on "Pending Install": Graph API URL issue

**Cause (fixed in v1.11.10):** Prior to v1.11.10, the Intune `retrieveDeviceAppInstallationStatusReport` API was called without the required `microsoft.graph.` namespace prefix. The Graph beta endpoint silently returned empty data instead of erroring, so the polling service saw no install data for any app/user and statuses remained stuck at PendingInstall or NotApplicable.

**Solution:** Upgrade to v1.11.10. After deploying, the next polling cycle (within 15 minutes) will query Intune with the correct URL and update all statuses.

---

#### Install status stuck on "Pending Install": general

**Cause:** The Intune install status polling service hasn't detected a status change yet, or the device hasn't checked in with Intune.

**Diagnosis:**
1. Check if the background polling service is running:
   ```kusto
   traces
   | where message contains "Checking install status"
   | order by timestamp desc
   | take 10
   ```

2. Verify the user/device is in the correct deployment group in Microsoft Entra ID

3. Check if the device is online and syncing with Intune

**Common causes:**
- Device hasn't synced with Intune since the assignment was created (can take up to 8 hours)
- User/device was not successfully added to the deployment group
- App assignment filter is excluding the device
- The polling service runs every 15 minutes (wait for the next cycle)

**Solution:**
- On the target device, open Company Portal and trigger a sync
- Verify group membership in Microsoft Entra ID
- Check the Intune device status report for the specific app

---

#### Install status shows "Pending Install" but Intune shows "Failed"

**Cause (fixed in v1.11.4):** Prior to v1.11.4, the install status parser had incorrect numeric mappings. Intune's `resultantAppState` value `"2"` (Failed) was mapped to Installing, and `"5"` (PendingInstall) was mapped to Failed. This caused failures to be displayed as "Installing" or to remain stuck at "Pending Install".

**Solution:** Upgrade to v1.11.4 or later. The fix corrects all numeric mappings to match Microsoft's `resultantAppState` enum. After upgrading, the next polling cycle (within 15 minutes) will update all affected requests to the correct status.

---

#### Install status stuck at "Not Applicable" / deployment status shows all zeros

**Cause (fixed in v1.11.9):** Prior to v1.11.9, requests that were auto-approved (apps without an approval workflow) never initialized `InstallStatus` to `PendingInstall`. The status defaulted to `NotApplicable`, so the install status polling service never tracked their deployment progress. This only affected auto-approved requests. Manually-approved requests via the approval workflow were set correctly.

**Solution:** Upgrade to v1.11.9. After upgrading, run the following SQL against your database to fix existing requests that are stuck:

```sql
UPDATE AppRequests
SET InstallStatus = 1  -- PendingInstall
WHERE Status = 4       -- Completed
  AND InstallStatus = 0 -- NotApplicable
  AND AppId IN (
    SELECT Id FROM Apps
    WHERE IntuneAppId IS NOT NULL
      AND IntuneAppId NOT LIKE 'winget-%'
  );
```

The polling service will then pick up these requests and check Intune for their actual install status within 15 minutes.

---

#### PSADT-wrapped app fails to install (error 0x8007EA68)

**Cause (fixed in v1.11.5):** Prior to v1.11.5, the generated `Deploy-Application.ps1` for MSI installers passed `-Parameters '/qn /norestart'` to `Execute-MSI`. PSADT v4 renamed this parameter and already applies `/qn /norestart` automatically in Silent deploy mode, causing a parameter conflict.

**Diagnosis:**
1. Check the Intune device install report for the app, look for `HexErrorCode: 0x8007EA68` (decimal 60008)
2. Check PSADT logs on the target device: `C:\Windows\Logs\Software\`
3. Error codes in the 60000 range indicate PSADT framework errors

**PSADT error codes:**

| Exit Code | Hex Code | Description |
|-----------|----------|-------------|
| 60001 | 0x8007EA61 | General PSADT error |
| 60002 | 0x8007EA62 | Pre-installation phase error |
| 60003 | 0x8007EA63 | Installation phase error |
| 60008 | 0x8007EA68 | Generic non-zero exit from wrapped installer |

**Solution:** Upgrade to v1.11.5 or later. Then delete the affected app from Intune using the Delete button in the portal and republish it. The regenerated PSADT script will no longer pass conflicting silent switches.

---

### Assignment filter dropdown is empty

**Symptom:** When configuring per-ring deployment settings (Update Ring Templates, or per-app Custom rings), the Intune assignment filter dropdown shows "No filters available" or a blank list, even though your tenant has filters configured.

**Cause:** The portal's API app registration is missing the `DeviceManagementConfiguration.Read.All` Microsoft Graph permission. This is required to read `/deviceManagement/assignmentFilters` and was not listed in setup docs prior to v1.22.1.

**Diagnosis:**

In Application Insights:

```kusto
traces
| where message contains "Assignment filters API"
| order by timestamp desc
| take 20
```

A 403 from Graph or "Forbidden" message confirms the missing permission.

**Solution:**

1. Microsoft Entra admin center → **App registrations**
2. Open the portal's API app registration (named `App Store for Intune - API` or similar)
3. **API permissions** → **Add a permission** → **Microsoft Graph** → **Application permissions**
4. Add `DeviceManagementConfiguration.Read.All`
5. Select **Grant admin consent**
6. Refresh the App Updates page in the portal. Filters should populate immediately (no portal restart needed; results aren't cached server-side).

**Why this is needed:** Intune assignment filters live under a different Graph permission scope than Intune apps. `DeviceManagementApps.*` only covers the apps endpoints; reading filters requires `DeviceManagementConfiguration.Read.All` separately.

---

### Migration issues

#### Error: "Invalid column name 'PopularityRank'"

**Cause:** Database migration hasn't been applied.

**Diagnosis:**
1. Check which migrations have been applied:
   ```sql
   SELECT MigrationId, ProductVersion
   FROM __EFMigrationsHistory
   ORDER BY MigrationId DESC
   ```

2. Look for migration `20260219003512_AddPopularityRankAndCategoryToWingetCache`

**Solution:**

**Option 1: Apply migration manually**
```sql
-- Add missing columns
ALTER TABLE WingetPackageCache ADD PopularityRank INT NULL;
ALTER TABLE WingetPackageCache ADD Category NVARCHAR(MAX) NULL;

-- Record migration
INSERT INTO __EFMigrationsHistory (MigrationId, ProductVersion)
VALUES ('20260219003512_AddPopularityRankAndCategoryToWingetCache', '8.0.0');
```

**Option 2: Restart App Service**
Migrations run automatically on startup. Restarting may trigger the migration.
