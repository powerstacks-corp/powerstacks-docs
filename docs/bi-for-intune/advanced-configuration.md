---
title: "Advanced configurations overview"
description: "Optional integrations that unlock additional dashboards in BI for Intune."
---
# Advanced configurations overview

The pages in this section describe **optional** configuration. BI for Intune is fully usable without any of it — the dashboards in the [Setup Guide](installation/setup-guide/create-entra-app-registration.md) cover everything Microsoft Graph exposes natively.

These add-ons unlock dashboards that depend on data sources Microsoft does not return through the Graph API. If you skip them, the rest of the product still works. The dashboards that depend on them simply show no data.

## What each add-on enables

### Windows Update for Business Reports

[Windows Update for Business reports](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview) is a Microsoft cloud service that surfaces Windows update compliance for Microsoft Entra joined devices. Microsoft writes this data into a Log Analytics workspace that you own. Connecting BI for Intune to that Log Analytics workspace populates the following dashboards:

- WUfB Quality Updates
- WUfB Feature Updates
- WUfB Driver Updates
- WUfB Delivery Optimization
- WUfB Windows Readiness

See [Set up Windows Update for Business reports](installation/log-analytics/wufb-reports.md) to enable this.

### Custom Inventory

Custom Inventory is a PowerShell-based collection pipeline that gathers device facts Intune doesn't track natively. The scripts run on your fleet and write data into a Log Analytics workspace, where BI for Intune reads it back. Custom Inventory populates the following dashboards:

- Firewall Status
- App Inventory
- Driver Inventory
- Microsoft 365
- Monitor
- Disk
- Battery
- Warranty

!!! note "Warranty dashboard requires manufacturer API keys"
    The Warranty dashboard looks up warranty data by serial number from each device manufacturer (Dell, Lenovo, HP, and others). You provide your own API keys per manufacturer. Setup instructions are on the Custom Inventory pages.

The current install path uses the **Azure Monitor Logs Ingestion API** (DCR-based) and is set up via a one-click ARM template. Existing customers using the older HTTP Data Collector API can migrate; see [Migrate to Log Ingestion API](installation/log-analytics/migrate-to-log-ingestion-api.md) under Administration.

## One Log Analytics workspace serves both

If you set up both add-ons, point them at the **same** Log Analytics workspace. BI for Intune reads both Windows Update for Business Reports data and Custom Inventory data from one workspace.
