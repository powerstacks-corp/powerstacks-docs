---
title: "Migrate to Log Ingestion API"
render_macros: false
---

# Migrate to the Log Ingestion API

If you previously set up Enhanced Inventory using the older Log Analytics HTTP Data Collector API, you need to migrate to the new **Azure Monitor Logs Ingestion API**. Microsoft is deprecating the legacy API in favor of the newer DCR-based ingestion pattern.

This guide walks existing customers through the migration. New customers should skip this page and go directly to the [Enhanced Inventory setup guide](../custom-inventory.md).

## What changed

| | Old method | New method |
| --- | --- | --- |
| **API** | HTTP Data Collector API | Azure Monitor Logs Ingestion API |
| **Authentication** | Workspace ID + Shared Key | Entra App + Client Secret (OAuth 2.0) |
| **Infrastructure** | Log Analytics Workspace only | Workspace + DCE + DCR |
| **Table creation** | Auto-created on first ingest | Pre-defined via ARM template |
| **Setup** | Manual PowerShell configuration | One-click Deploy to Azure |
| **Security** | Shared key (less secure) | OAuth 2.0 via Entra (more secure) |
| **Microsoft status** | Being deprecated | Current, supported long-term |

## What happens to your existing data

Your existing Enhanced Inventory data is **preserved**. The migration converts your existing custom tables (`PowerStacksDeviceInventory_CL`, `PowerStacksAppInventory_CL`, `PowerStacksDriverInventory_CL`) from the legacy Classic format to the DCR-based format **in place**: they keep the same names and all of their historical rows. Only the way each table is managed and ingested into changes. No second set of tables is created, so there is nothing to delete afterward.

During the cutover you can run the old and new inventory scripts in parallel. The legacy Data Collector API keeps writing to these tables through Microsoft's grace period, so there is no reporting gap while your devices move to the new script.

## Migration steps

### Step 1: Back up your current configuration

Before making changes, record your current inventory script settings:

- Log Analytics Workspace ID
- Primary/Secondary Key
- Script version and any customizations you have made
- Any custom Intune remediation schedules

### Step 2: Migrate your existing tables

Your inventory tables (`PowerStacksDeviceInventory_CL`, `PowerStacksAppInventory_CL`, `PowerStacksDriverInventory_CL`) were created by the legacy Data Collector API as **Classic** tables. The new deployment manages tables through the DCR-based tables API, and Azure does not allow changing a Classic table's schema with that API. If you skip this step, the deployment in Step 3 fails with an error like:

> Changing Classic table PowerStacksAppInventory_CL schema by using DataCollectionRuleBased tables api is forbidden, please migrate the table first.

Run the one-time migration script to convert these tables to the DCR-based format. It is idempotent (safe to re-run), preserves all existing data, and creates no managed identity or role assignment.

1. Open a PowerShell session with the **Az** module installed (Azure Cloud Shell already has it).
2. Download the migration script:

    ```powershell
    $raw = "https://raw.githubusercontent.com/powerstacks-corp/EnhancedInventoryDeploy/main/migrate/Migrate-PowerStacksClassicTables.ps1"
    Invoke-WebRequest -Uri $raw -OutFile .\Migrate-PowerStacksClassicTables.ps1
    ```

3. Run it against your existing workspace (add `-WhatIf` first to preview the changes):

    ```powershell
    .\Migrate-PowerStacksClassicTables.ps1 `
      -SubscriptionId <your-subscription-id> `
      -ResourceGroupName <workspace-resource-group> `
      -WorkspaceName <workspace-name>
    ```

The script signs you in if needed and migrates only the tables that are still Classic, so it is safe to re-run. Once it reports the tables as migrated, continue to Step 3.

!!! note "Sign-in on locked-down tenants"
    The script uses an interactive sign-in (a browser window, or your existing Azure Cloud Shell session) and does not use device-code authentication. If your tenant enforces conditional access and the script cannot sign in silently, run `Connect-AzAccount` first, then re-run the script.

### Step 3: Deploy the new infrastructure

Follow the [Enhanced Inventory setup guide](../custom-inventory.md). You will create new resources but keep your existing workspace:

1. Create the Enterprise Application and record credentials (Step 1 of the setup guide).
2. Deploy the Azure resources, selecting **Use an existing workspace** and providing your current Log Analytics workspace details (Step 2 of the setup guide).
3. Record the deployment outputs (DceURI, DcrImmutableId).

!!! tip "Use your existing workspace"
    During the Azure deployment, select **Use an existing workspace** and provide your current Log Analytics workspace details. This ensures the new tables are created in the same workspace your BI for Intune semantic model already connects to.

### Step 4: Update the inventory scripts

Update your Windows and/or macOS inventory scripts with the new parameters:

| Parameter | Old value | New value |
| --- | --- | --- |
| `LogAPIMode` | `DataCollectorAPI` (or not set) | `LogIngestionAPI` |
| `TenantId` | *(not used)* | Your Entra Tenant ID |
| `ClientId` | *(not used)* | Your Entra Client ID |
| `ClientSecret` | *(not used)* | Your Entra Client Secret |
| `DceURI` | *(not used)* | From deployment outputs |
| `DcrImmutableId` | *(not used)* | From deployment outputs |
| `WorkspaceId` | Your old Workspace ID | *(no longer used)* |
| `SharedKey` | Your old Workspace Key | *(no longer used)* |

See the [Enhanced Inventory setup guide](../custom-inventory.md) (Steps 3 and 4) for full configuration details.

### Step 5: Redeploy the script via Intune

Update the remediation or shell script assignment in Intune with the updated script. The next time devices check in, they will begin sending data via the new API.

!!! note
    You can run the old and new scripts in parallel during migration. The old script continues writing to the old tables while the new script writes to the new tables. This gives you time to verify before cutting over.

### Step 6: Verify data flow

Wait for at least one device cycle (up to 24 hours depending on your schedule), then verify data is appearing in the new tables:

```kusto
PowerStacksDeviceInventory_CL
| summarize count() by bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

### Step 7: Update BI for Intune

If BI for Intune needs to be pointed at the new table names, update the semantic model parameters accordingly. Check the [Semantic Model Parameters](../../administration/semantic-model-parameters.md) page for guidance.

### Step 8: Retire the old configuration (optional)

After you have confirmed the new pipeline is working and BI for Intune is using the new tables:

1. Remove the old remediation/script assignment from Intune

## Summary checklist

- [ ] Current configuration backed up
- [ ] Existing Classic tables migrated to DCR-based
- [ ] Entra Application created with Enterprise App Object ID
- [ ] Azure resources deployed to existing workspace
- [ ] Deployment outputs recorded (DceURI, DcrImmutableId)
- [ ] Inventory scripts updated with new parameters
- [ ] Scripts redeployed via Intune
- [ ] Data verified in the Log Analytics tables
- [ ] BI for Intune semantic model updated (if needed)
- [ ] Old scripts retired

## Need help?

If you run into issues during migration, use the **LogIngestionAPI_CheckDCR** validation script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy) to diagnose DCR configuration problems.

You can also select the **Pax** chat icon in the bottom-right corner to ask for help with your migration.
