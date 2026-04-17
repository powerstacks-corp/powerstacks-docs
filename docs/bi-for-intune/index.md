---
hide:
  - toc
  - navigation
---

<div class="hero-banner">
  <h1>BI for Intune <span class="hero-accent">Documentation</span></h1>
  <p>Comprehensive Power BI reporting for Microsoft Intune.</p>
</div>

<div class="quick-links">
  <a class="quick-link-card" href="installation/getting-started/install-bi-for-intune/">
    <span class="card-title">Install Guide</span>
  </a>
  <a class="quick-link-card" href="administration/backup-custom-reports/">
    <span class="card-title">Admin Guide</span>
  </a>
  <a class="quick-link-card" href="user-guides/">
    <span class="card-title">User Guide</span>
  </a>
  <a class="quick-link-card" href="release-notes/">
    <span class="card-title">What's New</span>
  </a>
</div>

## Comprehensive reporting for Microsoft Intune

BI for Intune is a Power BI template app that connects directly to your Intune environment via the Microsoft Graph API. No agents on endpoints, no vendor portal — your data stays in your Power BI workspace, governed by your Microsoft 365 tenant policies.

Pre-built dashboards cover device health, compliance, discovered applications, Windows Update for Business, and custom inventory collection. Drill through from fleet-level summaries to individual devices, track OS versions, hardware models, encryption status, and Autopilot enrollment — all with automatic refresh on your schedule.

Extend your reporting with PowerShell-based inventory scripts for BitLocker, local admins, monitors, USB devices, and more. Optional Log Analytics integration provides extended data retention and advanced querying capabilities.

---

## Getting Started

- [Install BI for Intune](installation/getting-started/install-bi-for-intune.md)
- [Request a Trial License](../shared/request-a-license.md)

## Setup Guide

- [Create Entra App Registration](installation/setup-guide/create-entra-app-registration.md)
- [Configure the Semantic Model](installation/setup-guide/configure-the-semantic-model.md)
- [Configure Data Sync](installation/setup-guide/configure-data-sync.md)
- [Export API Parameter](installation/setup-guide/export-api-parameter.md)

## Log Analytics

- [Connect Power BI to Log Analytics](installation/log-analytics/edit-entra-app-registration.md)
- [Semantic Model Settings](installation/log-analytics/semantic-model-settings-for-log-analytics.md)
- [WUfB Reports](installation/log-analytics/wufb-reports.md)

## Custom Inventory

- [Create Inventory App Registration](installation/custom-inventory/create-inventory-app-registration.md)
- [Deploy Custom Inventory Resources](installation/custom-inventory/deploy-custom-inventory-resources.md)
- [Windows Inventory Collection Script](installation/custom-inventory/windows-inventory-collection-script.md)
- [macOS Inventory Collection Script](installation/custom-inventory/macos-inventory-collection-script.md)

## Administration

- [Semantic Model Parameters](administration/semantic-model-parameters.md)
- [Backup Custom Reports](administration/backup-custom-reports.md)
- [Perform In-place Upgrade](administration/perform-in-place-upgrade.md)

## Release Notes

- [Latest Releases](release-notes/index.md)
