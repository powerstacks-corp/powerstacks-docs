---
hide:
  - toc
  - navigation
---

<div class="hero-banner">
  <h1>BI for SCCM <span class="hero-accent">Documentation</span></h1>
  <p>Comprehensive Power BI reporting for Microsoft Configuration Manager.</p>
</div>

<div class="quick-links">
  <a class="quick-link-card" href="installation/getting-started/install-bi-for-sccm/">
    <span class="card-title">Install Guide</span>
  </a>
  <a class="quick-link-card" href="administration/backup-custom-reports/">
    <span class="card-title">Admin Guide</span>
  </a>
  <a class="quick-link-card" href="user-guides/">
    <span class="card-title">User Guide</span>
  </a>
  <a class="quick-link-card" href="administration/semantic-model-parameters/">
    <span class="card-title">References</span>
  </a>
  <a class="quick-link-card" href="release-notes/">
    <span class="card-title">What's New</span>
  </a>
</div>

## Comprehensive reporting for Configuration Manager

BI for SCCM is a Power BI template app that connects to your ConfigMgr SQL database through Power BI Gateway. No middleware, no agents — your data stays in your Power BI workspace, governed by your Microsoft 365 tenant policies.

Pre-built dashboards cover software update compliance, hardware inventory, software inventory with license metering, and Active Directory user discovery. Track update group compliance, deployment progress, device models, BIOS versions, and installed applications across your entire fleet.

Extend your reporting with 10+ inventory extension scripts for BitLocker status, local admin group members, Lenovo model names, Microsoft 365 Apps, disk types, antivirus software, monitors, environment variables, USB devices, and warranty information. Optional Azure Maps integration provides geographic visualization of your device fleet.

---

## Getting Started

- [Install BI for SCCM](installation/getting-started/install-bi-for-sccm.md)
- [Request a License Key](../shared/request-a-license.md)
- [Install Power BI Gateway](installation/setup-guide/install-power-bi-gateway.md)
- [Configure Database Access](installation/setup-guide/configure-database-access.md)
- [Configure the Dataset](installation/setup-guide/configure-the-semantic-model.md)

## Guides

Step-by-step instructions for configuring and customizing BI for SCCM.

- [Dataset Parameters](administration/semantic-model-parameters.md)
- [AD User Discovery](installation/setup-guide/ad-user-discovery.md)
- [Backup Custom Reports](administration/backup-custom-reports.md)

### Inventory Extensions

Extend ConfigMgr hardware inventory with custom data collection.

- [Inventory BitLocker](installation/custom-inventory/bitlocker.md)
- [Inventory Local Admin Group](installation/custom-inventory/local-admin-group.md)
- [Inventory Lenovo Model Names](installation/custom-inventory/lenovo-model-names.md)
- [Inventory Microsoft 365 Apps](installation/custom-inventory/microsoft-365-apps.md)
- [Inventory Disk Types](installation/custom-inventory/disk-types.md)
- [Inventory Antivirus Software](installation/custom-inventory/antivirus-software.md)
- [Inventory Monitors](installation/custom-inventory/monitors.md)
- [Inventory Environment Variables](installation/custom-inventory/environment-variables.md)
- [Inventory USB Devices](installation/custom-inventory/usb-devices.md)
- [Collect Warranty Info](installation/custom-inventory/warranty-info.md)

## Release Notes

See what's new in each version of BI for SCCM.

- [All Release Notes](release-notes/index.md)
