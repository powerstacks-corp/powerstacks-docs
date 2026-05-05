---
title: "Advanced Configuration"
description: "Optional configuration that unlocks additional dashboards in BI for SCCM."
---

# Advanced Configuration

The pages in this section describe **optional** configuration. BI for SCCM is fully usable without any of it — once the Setup Guide is complete, you have a working set of dashboards built on the data Configuration Manager already collects by default.

The pages here describe additional configuration you can do *inside Configuration Manager* to extend what its hardware inventory collects. Several BI for SCCM dashboards depend on data classes that ConfigMgr does not enable in the default client settings. If you skip these steps, the rest of the product still works; the dashboards that depend on them simply show no data.

## How Custom Inventory works in BI for SCCM

Configuration Manager has a flexible hardware inventory system. Each item below describes a custom MOF or extension that you import into your Default Client Settings (or a custom Client Settings policy) so SCCM clients begin collecting that data on their next inventory cycle. Once the data is in the SCCM database, BI for SCCM picks it up automatically — no Power BI changes required.

| Add-on | What it unlocks |
| --- | --- |
| **BitLocker** | Encryption status and recovery key visibility for managed devices |
| **Local Admin Group** | Local administrator membership across the fleet |
| **Lenovo Model Names** | Friendly Lenovo model names instead of cryptic SKU codes |
| **Microsoft 365 Apps** | Channel and version distribution for Microsoft 365 Apps installs |
| **Disk Types** | SSD vs HDD breakdown across managed devices |
| **Antivirus Software** | Detected antivirus products and signature freshness |
| **Monitors** | Monitor model, serial, and connection inventory |
| **Environment Variables** | Per-device environment variable inventory (auditing-friendly) |
| **USB Devices** | Connected and historical USB device inventory |
| **Warranty Info** | Manufacturer warranty status (requires API tokens — see the Warranty Info page) |

## Want a callout for a specific dashboard?

We're working toward per-dashboard documentation that names exactly which Custom Inventory item each dashboard needs. Until that lands, the rule of thumb is: if a dashboard you care about is empty, check whether its data source is one of the Custom Inventory items above and confirm that data class is enabled in your SCCM client settings.
