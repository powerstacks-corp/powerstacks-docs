---
title: Troubleshoot Slow or Failing Syncs
description: Use the Graph API Error Finder PowerShell script to collect diagnostic data when BI for Intune syncs are slow or returning errors, and share the results with Microsoft Support.
---

# Troubleshoot Slow or Failing Syncs

When BI for Intune sync runs are slow, intermittent, or returning errors, the cause is usually on the Microsoft Graph API side rather than in BI for Intune itself. Microsoft Intune's mobile apps endpoint is subject to throttling, page-size thresholds that change without notice, and per-tenant scaling effects (large numbers of app assignments, in particular). Microsoft Support generally needs concrete evidence — page-by-page response times, retry events, throttling responses — to investigate.

The [Graph API Error Finder](https://github.com/powerstacks-corp/graph-error-finder) is a small PowerShell script that collects exactly this evidence. Run it from a workstation in the affected tenant, attach the resulting log file to a support case, and Microsoft has the data they need to look at the right pages, the right timestamps, and the right response codes.

This article explains when to use it, what permissions it needs, and how to run it.

---

## When to use it

Open this script when you observe any of the following on a tenant where you also run BI for Intune:

- BI for Intune sync runs that complete but take noticeably longer than they used to.
- Sync runs that fail with HTTP 429 (Too Many Requests), 500, 503, or 504 errors against `graph.microsoft.com/.../mobileApps`, `deviceManagementScripts`, or `deviceHealthScripts`.
- Gateway timeouts where Graph never returns a response inside the configured timeout.
- Inconsistent results between consecutive sync runs (one succeeds, the next fails on the same data).

If the sync is failing with a clear configuration error (missing permission, expired client secret, wrong tenant ID), fix that first. The Graph API Error Finder is for the cases where credentials are correct but Graph itself is unreliable for your tenant.

---

## What the script collects

For each Graph endpoint it tests, the script records:

- HTTP status codes per request attempt
- Response time per attempt and total per page
- `Retry-After` headers (when Graph provides them) and the exponential backoff applied when it doesn't
- Number of retries before a successful page
- Pagination behavior — how many `@odata.nextLink` pages were followed before the listing completed
- Total items returned per endpoint, broken down by `@odata.type`

For the proactive remediations endpoint, it also auto-discovers the largest page size that succeeds — useful for showing Microsoft the threshold at which their endpoint starts returning errors.

Optionally (set `$doScaleTest = $true` in the script), it will also iterate every item per endpoint and query `/assignments` individually, capturing per-item timings and counts. This data helps Microsoft identify whether a single item with an unusually large number of assignments is causing back-end pressure.

Output goes to a single timestamped log file under `C:\Temp` (configurable). The log includes a CSV-formatted retry table at the bottom that opens directly in Excel.

---

## Prerequisites

- **Windows PowerShell 5.1 or PowerShell 7+** on a workstation that can reach `login.microsoftonline.com` and `graph.microsoft.com`. No additional modules are required.
- **A read-only Entra ID app registration** with these Microsoft Graph **application** permissions, admin-consented:
    - `DeviceManagementApps.Read.All`
    - `DeviceManagementConfiguration.Read.All`
    - `DeviceManagementManagedDevices.Read.All`

The app registration that BI for Intune already uses on this tenant likely has these permissions and can be reused. If you would rather create a dedicated diagnostic app registration, follow the same flow as [Create Entra App Registration](../installation/setup-guide/create-entra-app-registration.md) but only grant the three permissions above.

You will need the **Tenant ID**, **Application (client) ID**, and a **client secret value** for whichever app registration you use. Treat the client secret as a credential — see the [security notes](#security-notes) below.

---

## Running the script

1. Download `Graph API Error Finder.ps1` from the [graph-error-finder repository](https://github.com/powerstacks-corp/graph-error-finder).
2. Open the script in your editor and fill in the configuration block at the top:

    ```powershell
    $TenantId     = "<your-tenant-guid>"
    $ClientId     = "<your-app-registration-client-id>"
    $ClientSecret = "<your-client-secret>"
    $PageSize     = 100      # default page size per endpoint
    $MaxRetries   = 7        # per-page retry ceiling
    $LogDir       = "C:\Temp"
    $doScaleTest  = $False   # set $True for the per-item assignment diagnostic
    ```

3. Run the script:

    ```powershell
    .\"Graph API Error Finder.ps1"
    ```

A typical run takes 1 to 10 minutes depending on the size of the tenant. The scale test (`$doScaleTest = $True`) can take significantly longer because it hits each item individually.

The script writes progress to the console as it goes. The complete log file is written to `$LogDir` with a timestamped name like `GraphDiag_20260504_143055.log`.

---

## What to attach to your Microsoft Support case

A single file: the log written to `$LogDir`. It contains:

- The end-to-end timing for every page request
- Every retry event, with HTTP status code and wait time
- A type breakdown for each endpoint so Microsoft can see whether a particular app type dominates
- A CSV-formatted retry table at the bottom so support engineers can paste it into Excel
- (If `$doScaleTest = $True`) a CSV listing of the slowest items and any "All Devices" or "All Users" assignments

Before attaching, scan the log for any sensitive values you would prefer to redact. The script does not log secrets, but the log will include your tenant ID and the app registration object ID, which are normally fine to share in a Microsoft Support case.

---

## Security notes

- **Read-only.** The script only issues `GET` requests. It never writes to or modifies your Intune tenant.
- **Application permissions.** It uses client-credentials authentication (app-only), not delegated. The app registration's granted permissions are the only thing that bound what it can read.
- **Credential hygiene.** Do not commit the script with your client secret pasted in. Set the value in your local copy and delete it after the diagnostic run, or read the secret from an environment variable. Rotate the client secret after the support case closes — assume any secret pasted into a script file is compromised.
- **Network.** The script only reaches `https://login.microsoftonline.com` and `https://graph.microsoft.com`.

---

## Related

- Repository (full README, license, and updates): [powerstacks-corp/graph-error-finder](https://github.com/powerstacks-corp/graph-error-finder)
- General Intune throttling guidance: [Microsoft Graph throttling guidance](https://learn.microsoft.com/en-us/graph/throttling)
