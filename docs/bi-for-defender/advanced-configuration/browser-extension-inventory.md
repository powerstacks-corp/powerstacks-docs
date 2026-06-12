---
title: "Browser Extension Inventory"
description: "What the Browser Extension dashboards show in BI for Defender, and the Microsoft Defender Vulnerability Management entitlement they depend on."
---
# Browser Extension Inventory

The Browser Extension dashboards in BI for Defender visualize the inventory of installed Chromium and Firefox-family browser extensions across your fleet: extension name, publisher, permissions requested, and per-device counts.

## Requires Microsoft Defender Vulnerability Management

This data is collected and exposed by **Microsoft Defender Vulnerability Management (MDVM)**, a paid add-on to Microsoft Defender for Endpoint Plan 2. Without the MDVM add-on, Microsoft does not surface browser-extension inventory in the data BI for Defender reads, so the corresponding dashboards remain blank.

If the Browser Extension dashboards are empty in your reports, confirm with your Microsoft licensing contact whether MDVM is included in your subscription. There is nothing to configure on the PowerStacks side. Once the entitlement is in place, the data flows automatically on the next refresh.
