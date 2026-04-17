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
    <span class="card-icon"><svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></span>
    <span class="card-title">Install Guide</span>
  </a>
  <a class="quick-link-card" href="administration/backup-custom-reports/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>
    <span class="card-title">Admin Guide</span>
  </a>
  <a class="quick-link-card" href="user-guides/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span>
    <span class="card-title">User Guide</span>
  </a>
  <a class="quick-link-card" href="release-notes/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
    <span class="card-title">What's New</span>
  </a>
</div>

## Comprehensive reporting for Microsoft Intune

BI for Intune is a Power BI template app that connects directly to your Intune environment via the Microsoft Graph API. No agents on endpoints, no vendor portal — your data stays in your Power BI workspace, governed by your Microsoft 365 tenant policies.

Pre-built dashboards cover device health, compliance, discovered applications, Windows Update for Business, and custom inventory collection. Drill through from fleet-level summaries to individual devices, track OS versions, hardware models, encryption status, and Autopilot enrollment — all with automatic refresh on your schedule.

Extend your reporting with PowerShell-based inventory scripts for BitLocker, local admins, monitors, USB devices, and more. Optional Log Analytics integration provides extended data retention and advanced querying capabilities.

---

<div class="ps-two-col" markdown>
<div markdown>

## Getting Started

- [Install BI for Intune](installation/getting-started/install-bi-for-intune.md)
- [Request a Trial License](../shared/request-a-license.md)

## Log Analytics

- [Connect Power BI to Log Analytics](installation/log-analytics/edit-entra-app-registration.md)
- [Semantic Model Settings](installation/log-analytics/semantic-model-settings-for-log-analytics.md)
- [WUfB Reports](installation/log-analytics/wufb-reports.md)

## Administration

- [Semantic Model Parameters](administration/semantic-model-parameters.md)
- [Backup Custom Reports](administration/backup-custom-reports.md)
- [Perform In-place Upgrade](administration/perform-in-place-upgrade.md)

</div>
<div markdown>

## Setup Guide

- [Create Entra App Registration](installation/setup-guide/create-entra-app-registration.md)
- [Configure the Semantic Model](installation/setup-guide/configure-the-semantic-model.md)
- [Configure Data Sync](installation/setup-guide/configure-data-sync.md)
- [Export API Parameter](installation/setup-guide/export-api-parameter.md)

## Custom Inventory

- [Create Inventory App Registration](installation/custom-inventory/create-inventory-app-registration.md)
- [Deploy Custom Inventory Resources](installation/custom-inventory/deploy-custom-inventory-resources.md)
- [Windows Inventory Collection Script](installation/custom-inventory/windows-inventory-collection-script.md)
- [macOS Inventory Collection Script](installation/custom-inventory/macos-inventory-collection-script.md)

## Release Notes

- [Latest Releases](release-notes/index.md)

</div>
</div>
