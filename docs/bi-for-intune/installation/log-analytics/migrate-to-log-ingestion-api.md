---
title: "Migrate to Log Ingestion API"
render_macros: false
---

# Migrate to the Log Ingestion API

If you previously set up Custom Inventory using the older Log Analytics HTTP Data Collector API, you need to migrate to the new **Azure Monitor Logs Ingestion API**. Microsoft is deprecating the legacy API in favor of the newer DCR-based ingestion pattern.

This guide walks existing customers through the migration. New customers should skip this page and go directly to the [Enhanced Inventory setup guide](../custom-inventory/create-inventory-app-registration.md).

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

Your existing Custom Inventory data in Log Analytics is **not affected** by this migration. The new setup creates new custom tables alongside any existing ones. Historical data remains queryable in the old tables.

Once the new pipeline is verified and BI for Intune is configured to use the new tables, you can optionally delete the old tables to stop incurring storage costs.

## Migration steps

### Step 1: Back up your current configuration

Before making changes, record your current inventory script settings:

- Log Analytics Workspace ID
- Primary/Secondary Key
- Script version and any customizations you have made
- Any custom Intune remediation schedules

### Step 2: Deploy the new infrastructure

Follow the standard Enhanced Inventory setup. You will create new resources but keep your existing workspace:

1. [Create an Entra Application](../custom-inventory/create-inventory-app-registration.md) — create the Enterprise Application and record credentials
2. [Deploy Azure Resources](../custom-inventory/deploy-custom-inventory-resources.md) — use your **existing** Log Analytics workspace
3. Record the deployment outputs (DceURI, DcrImmutableId)

!!! tip "Use your existing workspace"
    During the Azure deployment, select **Use an existing workspace** and provide your current Log Analytics workspace details. This ensures the new tables are created in the same workspace your BI for Intune semantic model already connects to.

### Step 3: Update the inventory scripts

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

See [Windows Inventory Script](../custom-inventory/windows-inventory-collection-script.md) and [macOS Inventory Script](../custom-inventory/macos-inventory-collection-script.md) for full configuration details.

### Step 4: Redeploy the script via Intune

Update the remediation or shell script assignment in Intune with the updated script. The next time devices check in, they will begin sending data via the new API.

!!! note
    You can run the old and new scripts in parallel during migration. The old script continues writing to the old tables while the new script writes to the new tables. This gives you time to verify before cutting over.

### Step 5: Verify data flow

Wait for at least one device cycle (up to 24 hours depending on your schedule), then verify data is appearing in the new tables:

```kusto
PowerStacksDeviceInventory_CL
| summarize count() by bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

### Step 6: Update BI for Intune

If BI for Intune needs to be pointed at the new table names, update the semantic model parameters accordingly. Check the [Semantic Model Parameters](../../administration/semantic-model-parameters.md) page for guidance.

### Step 7: Retire the old configuration (optional)

Once you have confirmed the new pipeline is working and BI for Intune is using the new tables:

1. Remove the old remediation/script assignment from Intune
2. Revoke or delete the old Workspace Shared Key (if no other services use it)
3. Optionally delete the old custom tables from Log Analytics to stop storage costs

## Summary checklist

- [ ] Current configuration backed up
- [ ] Entra Application created with Enterprise App Object ID
- [ ] Azure resources deployed to existing workspace
- [ ] Deployment outputs recorded (DceURI, DcrImmutableId)
- [ ] Inventory scripts updated with new parameters
- [ ] Scripts redeployed via Intune
- [ ] Data verified in new Log Analytics tables
- [ ] BI for Intune semantic model updated (if needed)
- [ ] Old scripts retired and shared keys revoked

## Need help?

If you run into issues during migration, use the **LogIngestionAPI_CheckDCR** validation script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy) to diagnose DCR configuration problems.

You can also click the **Pax** chat icon in the bottom-right corner to ask for help with your migration.
