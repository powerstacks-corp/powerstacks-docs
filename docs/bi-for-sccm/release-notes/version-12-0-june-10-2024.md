---
title: "Version 12.0 June 10, 2024"
---
# Version 12.0 (AppSource Version 1018)
BI for SCCM Version 12.0, shown as version 1018 in AppSource, was released on June, 10, 2024. This version brings a change that allows customers to connect BI for SCCM to BI for Intune and/or BI for Defender for single pane of glass reporting.

- **Features:**Added new "Device USB" category to the data model. This requires "[USB Device - Asset Intelligence (Win32_USBDevice)](inventory-usb-devices.md)" to be added to hardware inventory.
**Enhancements:**
- Added "Driver Date (Days)" to the Computer Video Card category.
- On the "Encryption Status" page we added filters for "Computer Name" and "OS Name" to the filters pane.
- Added "Azure AD Tenant ID" and "Azure AD Device ID" to the "Computer" category.
- Added "Device.id" to the "Computer" and "User Computers" categories. This can be used to connect the BI for SCCM data model to both BI for Intune and BI for Defender data models.
**Bug Fixes:**
- N/A
**Important Notes:**
- Always backup your custom reports using our [backup process](backup-custom-reports.md).
