---
title: "Advanced Configuration"
description: "Optional configuration that unlocks or enriches additional dashboards in BI for Defender."
---
# Advanced Configuration

Most of BI for Defender works as soon as the [Setup Guide](../installation/setup-guide/create-entra-app-registration.md) is complete. The pages in this section cover **optional** configuration that unlocks or enriches specific dashboards. If you skip any of it, the rest of the product still works; the dashboards that depend on it simply show no data.

## What each one enables

- **[Application Controls](../installation/setup-guide/application-controls.md)** — populate the Application Controls page with Windows Defender Application Control (WDAC) reporting. Requires WDAC policies deployed to your devices.
- **[Browser Extension Inventory](browser-extension-inventory.md)** — populate the Browser Extension dashboards. Requires the Microsoft Defender Vulnerability Management (MDVM) add-on.
- **[Cloud App Usage](cloud-app-usage.md)** — surface the per-user and compliance detail behind the discovered cloud apps. Requires tagging the apps in Microsoft Defender and adding the tag to the semantic model.
