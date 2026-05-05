---
title: "Advanced Configuration"
description: "Optional prerequisites that unlock additional dashboards in BI for Defender."
---

# Advanced Configuration

Most of BI for Defender works as soon as the [Setup Guide](installation/setup-guide/create-entra-app-registration.md) is complete — there is no PowerStacks-side optional configuration to do.

There is, however, one **Microsoft-side** prerequisite that affects what data flows into BI for Defender. It's documented here so you know in advance which dashboards depend on it.

## Browser Extension Inventory (requires Microsoft Defender Vulnerability Management)

The Browser Extension dashboards in BI for Defender visualize the inventory of installed Chromium and Firefox-family browser extensions across your fleet — extension name, publisher, permissions requested, and per-device counts.

This data is collected and exposed by **Microsoft Defender Vulnerability Management (MDVM)**, which is a paid add-on to Microsoft Defender for Endpoint Plan 2. Without the MDVM add-on, Microsoft does not surface browser-extension inventory in the data we read, so the corresponding BI for Defender dashboards remain blank.

If the Browser Extension dashboards are empty in your reports, confirm with your Microsoft licensing contact whether MDVM is included in your subscription. There is nothing to configure on the PowerStacks side — once the entitlement is in place, the data flows automatically on the next refresh.

## Want a callout for a specific dashboard?

We're working toward per-dashboard documentation that names exactly which prerequisite (if any) each dashboard depends on. Until that lands, the rule of thumb is: if a dashboard you care about is empty, check whether its data source requires a Microsoft add-on like MDVM.
