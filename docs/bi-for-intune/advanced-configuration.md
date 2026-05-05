---
title: "Advanced Configuration"
description: "Optional integrations that unlock additional dashboards in BI for Intune."
---

# Advanced Configuration

The pages in this section describe **optional** configuration. BI for Intune is fully usable without any of it — the dashboards in the Setup Guide cover everything Microsoft Graph exposes natively.

These add-ons unlock additional dashboards that depend on data sources Microsoft does not return through the Graph API. If you skip them, the rest of the product still works; the dashboards that depend on them simply show no data.

## What each add-on enables

### Log Analytics

Connecting BI for Intune to a Log Analytics workspace unlocks reports that pull data from sources Microsoft writes to Log Analytics, not Graph. There are two reasons to set this up:

- **WUfB Reports** — Microsoft only exposes Windows Update for Business Reports data (formerly *Azure Update Compliance*) through Log Analytics. If you want the WUfB Reports dashboards to populate, you need this. *(Note: this is separate from the Windows Autopatch data Microsoft is starting to surface in Intune natively — BI for Intune covers both because neither alone gives the full update picture.)*
- **Custom Inventory** — the Custom Inventory pipeline writes its data into a Log Analytics workspace, so the same Log Analytics connection is used to read Custom Inventory data into Power BI.

If you set up either WUfB Reports or Custom Inventory, you set up the Log Analytics connection once and both work against the same workspace.

### Custom Inventory

Custom Inventory is a PowerShell-based collection pipeline that gathers device facts Intune doesn't track natively — local administrator group membership, monitor model and serial, USB device history, warranty info, environment variables, and more. These dashboards are blank until the inventory scripts run on your fleet and start writing data into your Log Analytics workspace.

The new install path uses the **Azure Monitor Logs Ingestion API** (DCR-based) and is set up via a one-click ARM template. Existing customers using the older HTTP Data Collector API can migrate; see [Migrate to Log Ingestion API](installation/log-analytics/migrate-to-log-ingestion-api.md) under Administration.

## Want a callout for a specific dashboard?

We're working toward per-dashboard documentation that names exactly which add-on (if any) each dashboard depends on. Until that lands, the rule of thumb is: if a dashboard you care about is empty, check whether its data source is one of the optional add-ons above.
