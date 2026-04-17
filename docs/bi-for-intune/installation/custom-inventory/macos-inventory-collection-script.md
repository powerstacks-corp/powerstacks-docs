---
title: "macOS Inventory Collection Script"
render_macros: false
---

# macOS Inventory Collection Script

The macOS inventory script collects device and application inventory data from macOS endpoints and sends it to your Log Analytics workspace via the Log Ingestion API.

## Prerequisites

Before configuring the script, complete these steps:

1. [Create an Entra Application](create-inventory-app-registration.md)
2. [Deploy Azure Resources](deploy-custom-inventory-resources.md)

You should have recorded: Tenant ID, Client ID, Client Secret, DceURI, and DcrImmutableId.

## Configure the script

Update the following settings in the macOS inventory script:

| Parameter | Value |
| --- | --- |
| `LogAPIMode` | `LogIngestionAPI` |
| `TenantId` | Your Directory (Tenant) ID |
| `ClientId` | Your Application (Client) ID |
| `ClientSecret` | Your Client Secret value |
| `DceURI` | From deployment outputs |
| `DcrImmutableId` | From deployment outputs |

## Deploy via Intune

Deploy the macOS inventory script using Intune's **Shell scripts** feature:

1. In the [Intune admin center](https://intune.microsoft.com), go to **Devices** > **macOS** > **Shell scripts**.
2. Upload the macOS inventory script.
3. Assign it to your target device groups.
4. Set the schedule to **run once per day**.

## Data collected

The macOS script sends data to the same custom tables as the Windows script:

- **PowerStacksDeviceInventory_CL** — device hardware, OS version, encryption status
- **PowerStacksAppInventory_CL** — installed applications and versions

## Verify data ingestion

After the script has run on at least one device:

1. In the Azure Portal, navigate to your **Log Analytics workspace**.
2. Go to **Logs** and run:

```kusto
PowerStacksDeviceInventory_CL
| where DeviceOS_s == "macOS"
| take 10
```

If data appears, the macOS pipeline is working.

For troubleshooting, use the **LogIngestionAPI_CheckDCR** script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy).
