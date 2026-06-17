---
title: "Set up Enhanced Inventory"
description: "Collect device facts Intune doesn't track natively, send them to Log Analytics, and surface them in BI for Intune."
---
# Set up Enhanced Inventory

Enhanced Inventory is a PowerShell-based (Windows) and shell-based (macOS) collection pipeline that gathers device facts Intune doesn't track natively — hardware specs, monitor model and serial, disk health, battery health, Microsoft 365 channel, driver inventory, and warranty data — and sends them to your Azure Log Analytics workspace via the Log Ingestion API. BI for Intune reads from that workspace to populate the Firewall Status, App Inventory, Driver Inventory, Microsoft 365, Monitor, Disk, Battery, and Warranty dashboards.

## Prerequisites

- BI for Intune installed and configured (the [Setup Guide](setup-guide/create-entra-app-registration.md) is complete).
- A Log Analytics workspace set up per [Set up the Log Analytics workspace](log-analytics/set-up-log-analytics-workspace.md), including the BI for Intune app registration's **Log Analytics API Data.Read** permission and its **Log Analytics Reader** role on the workspace. If you also use [Windows Update for Business reports](log-analytics/wufb-reports.md), both add-ons share that same workspace.
- Microsoft Entra: **Application Administrator** or **Global Administrator**.
- Azure: **Contributor** or **Owner** on the target subscription or resource group, plus **User Access Administrator** or **Owner** to assign roles (only required for automatic RBAC assignment in Step 2).

!!! tip "One workspace for both add-ons"
    If you also set up [Windows Update for Business reports](log-analytics/wufb-reports.md), point it at this same workspace. BI for Intune reads both Enhanced Inventory data and Windows Update for Business Reports data from one Log Analytics workspace.

## Step 1: Create the Enterprise application

The Enhanced Inventory scripts use a dedicated Microsoft Entra application to authenticate to Azure and send data via the Log Ingestion API. This is separate from the main BI for Intune app registration.

!!! warning "Enterprise Application, not App Registration"
    You must create an **Enterprise Application** first, not a standard App Registration. The ARM deployment template in Step 2 requires the **Enterprise Application Object ID** (the service principal Object ID), which is different from the App Registration Object ID.

1. In the [Azure portal](https://portal.azure.com), go to **Microsoft Entra ID** > **Enterprise applications**.
1. Select **New application** > **Create your own application**.
1. Enter a name (for example, `PowerStacks-CustomInventory`).
1. Select **Integrate any other application you don't find in the gallery**.
1. Select **Create**.
1. From the Enterprise Application overview page, record the **Object ID**.

Switch to the **App Registrations** pane to get the credentials the inventory scripts will use:

1. Go to **Microsoft Entra ID** > **App registrations**.
1. Find the application you just created (search by name).
1. From the **Overview** page, record the **Directory (Tenant) ID** and the **Application (Client) ID**.
1. Go to **Certificates & secrets** > **New client secret**. Enter a description, select an expiration period, and select **Add**.
1. Immediately record the **Value** (not the Secret ID). The value is only shown once.

By the end of this step you should have:

| Value | Where to find it | Used by |
|---|---|---|
| **Enterprise App Object ID** | Enterprise Applications > Overview | ARM deployment template |
| **Directory (Tenant) ID** | App Registrations > Overview | Inventory scripts |
| **Application (Client) ID** | App Registrations > Overview | Inventory scripts |
| **Client Secret Value** | App Registrations > Certificates & secrets | Inventory scripts |

## Step 2: Deploy the Azure resources

This step uses a one-click ARM template to configure the custom tables, Data Collection Endpoint (DCE), and Data Collection Rule (DCR) in your existing Log Analytics workspace.

!!! note "Migrating an existing deployment?"
    If you already have Enhanced Inventory running and are upgrading the ingestion path (rather than setting it up for the first time), **Step 5: Grant BI for Intune read access to the workspace** and **Step 6: Connect BI for Intune to the Log Analytics workspace** were both completed during your original setup. You can skip them. Complete Steps 2 through 4 as written.

!!! tip "Prefer to watch a walkthrough first?"
    The interactive demo below is an optional supplement to the written steps on this page, not a replacement. The written instructions remain the canonical source of truth.

{{ storylane("https://powerstacks.storylane.io/share/btzozkmur3l9", title="Walkthrough: Deploy Enhanced Inventory (Azure Monitor)") }}

The deployment creates:

- Custom Log Analytics tables: `PowerStacksDeviceInventory_CL`, `PowerStacksAppInventory_CL`, `PowerStacksDriverInventory_CL`
- A Data Collection Endpoint (DCE)
- A Data Collection Rule (DCR)
- Automatic RBAC assignment (if the Enterprise App Object ID is provided)

Select the button below to deploy:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FPowerStacks-BI%2FEnhancedInventoryDeploy%2Fmain%2Finfra%2Fmain.json)

During deployment you will be prompted for:

- **Workspace selection** — select **Use an existing workspace** to reuse the workspace from your WUfB Reports setup.
- **Workspace details** — provide the subscription ID, resource group name, and workspace name.
- **Enterprise App Object ID** — paste the Object ID from Step 1.

After deployment completes, capture the outputs:

1. In the Azure portal, go to **Resource group** > **Deployments**.
1. Select the deployment name.
1. Select the **Outputs** tab and record:

    | Output | Used by |
    |---|---|
    | **DceURI** | Inventory scripts |
    | **DcrImmutableId** | Inventory scripts |

!!! info "If you skipped the Enterprise App Object ID"
    If you left the field blank during deployment, manually assign the **Monitoring Metrics Publisher** role to your Enterprise Application on the Data Collection Rule: **DCR** > **Access control (IAM)** > **Add role assignment**.

## Step 3: Deploy the Windows inventory script

The script gathers data from each Windows endpoint and sends it to the Log Analytics workspace via the Log Ingestion API.

Download `Intune_Windows_Inventory.ps1` from the [PowerStacks Windows-Enhanced-Inventory repository](https://github.com/powerstacks-corp/Windows-Enhanced-Inventory).

Update the following settings near the top of the script:

| Parameter | Value |
|---|---|
| `LogAPIMode` | `LogIngestionAPI` |
| `TenantId` | Directory (Tenant) ID from Step 1 |
| `ClientId` | Application (Client) ID from Step 1 |
| `ClientSecret` | Client Secret value from Step 1 |
| `DceURI` | From Step 2 outputs |
| `DcrImmutableId` | From Step 2 outputs |

### Collection toggles

Each major inventory category can be turned on or off independently. The defaults work for most BI for Intune deployments.

| Variable | Description | Default |
|---|---|---|
| `CollectDeviceInventory` | Hardware inventory (CPU, memory, disks, monitors, chassis, OS install date, battery) | `$true` |
| `CollectAppInventory` | Installed Win32 applications | `$true` |
| `CollectDriverInventory` | Installed and optional drivers | `$true` |
| `CollectMicrosoft365` | Microsoft 365 update channel and compliance (sub-toggle of device inventory) | `$true` |
| `CollectWarranty` | Warranty lookups via vendor APIs (sub-toggle of device inventory) | `$false` |
| `CollectUWPInventory` | UWP (modern app) inventory in addition to Win32 (sub-toggle of app inventory) | `$false` |
| `MatchDrivers` | Match installed driver packages to PnP devices for richer driver records | `$true` |
| `RemoveBuiltInMonitors` | Exclude internal laptop monitors from monitor inventory | `$false` |
| `WarrantyMaxCacheAgeDays` | Days before cached warranty data is refreshed from the vendor API | `180` |
| `WarrantyForceRefresh` | Ignore the local cache and force a fresh warranty API lookup | `$false` |

### Warranty API credentials

If `CollectWarranty` is enabled, you need API credentials from each vendor whose devices you want to look up. The Warranty dashboard remains blank for vendors you don't supply credentials for; the script skips them silently.

- **Dell** — apply at [Dell TechDirect](https://techdirect.dell.com/Portal/APIs.aspx) for a Client ID and Client Secret.
- **Lenovo** — contact your Lenovo account representative to request a Client ID. There is no self-service portal.
- **HP** — sign up at the [HP Developer Portal](https://developers.hp.com/) or work with your HP rep for a Client ID and Client Secret. HP secrets expire frequently and must be refreshed.
- **Getac** — contact your Getac account representative for API credentials.

Fill in the credentials you have:

```powershell
$WarrantyDellClientID     = "<your Dell client ID>"
$WarrantyDellClientSecret = "<your Dell client secret>"
$WarrantyLenovoClientID   = "<your Lenovo client ID>"
$WarrantyHPClientID       = "<your HP client ID>"
$WarrantyHPClientSecret   = "<your HP client secret>"
```

### Deploy via Intune

Deploy the script as a **detection script** in an Intune remediation:

1. In the [Intune admin center](https://intune.microsoft.com), go to **Devices** > **Remediations**.
1. Create a new remediation package.
1. Upload `Intune_Windows_Inventory.ps1` as the **detection script**.
1. Set **Run this script using the logged-on credentials** to **No**. The script runs as SYSTEM.
1. Set **Run script in 64-bit PowerShell** to **Yes**.
1. Assign the remediation to your target device groups.
1. Set the schedule to **run once per day**.

## Step 4: (Optional) Deploy the macOS inventory script

If you also manage macOS devices, deploy the macOS script to extend the same custom-inventory pattern to Mac endpoints.

Download `Mac_Custom_Inventory.sh` from the [PowerStacks Mac-Enhanced-Inventory repository](https://github.com/powerstacks-corp/Mac-Enhanced-Inventory).

Update the following settings near the top of `Mac_Custom_Inventory.sh`:

| Parameter | Value |
|---|---|
| `LogAPIMode` | `LogIngestionAPI` |
| `TenantId` | Directory (Tenant) ID from Step 1 |
| `ClientId` | Application (Client) ID from Step 1 |
| `ClientSecret` | Client Secret value from Step 1 |
| `DceURI` | From Step 2 outputs |
| `DcrImmutableId` | From Step 2 outputs |

| Variable | Description | Default |
|---|---|---|
| `CollectDeviceInventory` | Hardware inventory (CPU, memory, disks, battery, model) | `true` |
| `CollectAppInventory` | Installed-application list | `true` |
| `InventoryDateFormat` | `date` format string for the final status timestamp | `"%m-%d %H:%M"` |

Deploy the script via Intune **Shell scripts**:

1. In the [Intune admin center](https://intune.microsoft.com), go to **Devices** > **macOS** > **Shell scripts**.
1. Upload `Mac_Custom_Inventory.sh`.
1. Set **Run script as signed-in user** to **No**. The script runs as `root`.
1. Set **Script frequency** to **Every 1 day**.
1. Assign the script to your target device groups.

## Step 5: Grant BI for Intune read access to the workspace

The main BI for Intune app registration reads inventory data from this Log Analytics workspace using the **Log Analytics Reader** role. This is configured in [Set up the Log Analytics workspace](log-analytics/set-up-log-analytics-workspace.md#step-3-grant-the-app-registration-read-access-to-the-workspace). If you completed that page, this is already done; confirm the role is assigned and continue. Without it, data flows into the workspace but the Enhanced Inventory dashboards stay blank.

!!! note "Two roles, two apps"
    This is the read counterpart to the **Monitoring Metrics Publisher** role on the DCR. The Enterprise Application from Step 1 *writes* inventory data (Monitoring Metrics Publisher on the DCR); the BI for Intune app registration *reads* it (Log Analytics Reader on the workspace). They are separate applications with separate roles.

## Step 6: Connect BI for Intune to the Log Analytics workspace

!!! note "May already be done"
    If you set up WUfB Reports before Enhanced Inventory, this step is already done. Check that the **AzureAD LogAnalytics WorkspaceID** parameter in your BI for Intune dataset matches the workspace from Step 2. If it does, skip to **Verify data ingestion** below.

1. In the Power BI service, open the **BI for Intune** workspace.
1. Open the BI for Intune **semantic model settings**.
1. Expand **Parameters** and update:
    - **AzureAD LogAnalytics Enable** = `TRUE`
    - **AzureAD LogAnalytics WorkspaceID** = the **Workspace ID** of the Log Analytics workspace from Step 2. Find it at **Azure portal** > **Log Analytics workspaces** > your workspace > **Overview** > **Workspace ID**.
1. Select **Apply**.

## Verify data ingestion

After the script has run on at least one device, verify data is flowing:

1. In the Azure portal, go to your **Log Analytics workspace**.
1. Go to **Logs** and run:

    ```kusto
    PowerStacksDeviceInventory_CL
    | take 10
    ```

If data appears, the pipeline is working. For deeper troubleshooting, run the **LogIngestionAPI_CheckDCR** PowerShell script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy).

## What you'll see in BI for Intune

After data starts flowing, the following BI for Intune dashboards populate:

- Firewall Status
- App Inventory
- Driver Inventory
- Microsoft 365
- Monitor
- Disk
- Battery
- Warranty (per-vendor data depends on warranty API credentials supplied in Step 3)

## What gets collected

The scripts write three custom tables to your Log Analytics workspace:

- **PowerStacksDeviceInventory_CL** — hardware (CPU, memory, disks, monitors, battery, chassis), Microsoft 365 channel, warranty
- **PowerStacksAppInventory_CL** — installed applications
- **PowerStacksDriverInventory_CL** — installed and optional drivers (Windows only)

For the full field-by-field schemas, see the scripts in the [Windows-Enhanced-Inventory](https://github.com/powerstacks-corp/Windows-Enhanced-Inventory) and [Mac-Enhanced-Inventory](https://github.com/powerstacks-corp/Mac-Enhanced-Inventory) repositories.
