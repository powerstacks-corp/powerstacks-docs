---
title: "Windows Inventory Collection Script"
render_macros: false
---

# Windows Inventory Collection Script

The Windows inventory script collects device, application, and driver inventory data from Windows endpoints and sends it to your Log Analytics workspace via the Log Ingestion API.

## Prerequisites

Before configuring the script, complete these steps:

1. [Create an Entra Application](create-inventory-app-registration.md)
2. [Deploy Azure Resources](deploy-custom-inventory-resources.md)

You should have recorded: Tenant ID, Client ID, Client Secret, DceURI, and DcrImmutableId.

## Configure the script

Update the following settings in the Windows inventory script:

| Parameter | Value |
| --- | --- |
| `LogAPIMode` | `LogIngestionAPI` |
| `TenantId` | Your Directory (Tenant) ID |
| `ClientId` | Your Application (Client) ID |
| `ClientSecret` | Your Client Secret value |
| `DceURI` | From deployment outputs |
| `DcrImmutableId` | From deployment outputs |

## Deploy via Intune

Deploy the inventory script as a **detection script** in an Intune remediation:

1. In the [Intune admin center](https://intune.microsoft.com), go to **Devices** > **Remediations**.
2. Create a new remediation package.
3. Upload the Windows inventory script as the **detection script**.
4. Assign the remediation to your target device groups.
5. Set the schedule to **run once per day**.

The script will run silently on each device and send inventory data to your Log Analytics workspace.

## Data collected

The Windows script collects and sends data to three custom tables:

- **PowerStacksDeviceInventory_CL** — device hardware, OS, encryption, Autopilot enrollment
- **PowerStacksAppInventory_CL** — installed applications and versions
- **PowerStacksDriverInventory_CL** — installed drivers and versions

## Verify data ingestion

After the script has run on at least one device, verify data is flowing:

1. In the Azure Portal, navigate to your **Log Analytics workspace**.
2. Go to **Logs** and run a query against one of the custom tables:

```kusto
PowerStacksDeviceInventory_CL
| take 10
```

If data appears, the pipeline is working.

For deeper troubleshooting, run the **LogIngestionAPI_CheckDCR** PowerShell script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy). This script retrieves and displays the full DCR configuration, which is useful for diagnosing ingestion issues.

## Next step

If you also manage macOS devices, configure the [macOS Inventory Collection Script](macos-inventory-collection-script.md).
