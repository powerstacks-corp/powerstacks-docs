---
title: "Release Notes"
---

# BI for SCCM Release Notes

## Version 17.0 February 20, 2026

# Version 17.0 (AppSource Version 1023)
**Release Date**: February 20, 2026
**App Source Version**: 1023

BI for SCCM v17 expands hardware and BitLocker visibility while improving encryption reporting clarity.
This release introduces the new Computer Network Card object, enhances Logical Disk encryption reporting, and improves MAC address accuracy by filtering virtual adapters.
It also replaces the Is Encrypted field with updated Protection and Conversion status fields for more precise BitLocker state reporting. Review breaking changes if you reference encryption fields in custom reports.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 17.0


### Product Enhancements

- Updated the **Summary** page by replacing **Encryption Status** with **Protection Status**.
- Updated the **Device Info** page to exclude **Network Card Service** values of AsyncMac to prevent duplicate MAC address reporting from virtual adapters.
- Enhanced the **Encryption Status** page with additional BitLocker visibility fields.

### New Features

- Added new object **Computer Network Card** to provide visibility into network adapter details.

### Semantic Model Changes

- Added **Viewer Name** field to the **Authorization** object.
- Added new fields to the **Computer Network Card** object: Network Card Count, Network Card ID, Network Card Manufacturer, Network Card Name, Network Card Service.
- Added new fields to the **Computer Logical Disk** object: Conversion Status, Encryption Method, Encryption Readiness, Encryption Status, Protection Status.
- Removed **Is Encrypted** field from the **Computer Logical Disk** object. See the Important Notes section.

### Important Notes

- Removed **Is Encrypted** field from the **Computer Logical Disk** object. This is a breaking change. Custom reports referencing this field must be updated.
- A new hardware class must be enabled in SCCM to populate BitLocker-related fields on the **Encryption Status** page.
- Updated BitLocker status logic to align Encryption Status, Protection Status, and Conversion Status values for clearer reporting states.
- Encryption Readiness now reflects volume initialization state where IsVolumeInitializedForProtec0 = 0 is reported as Not Ready and 1 is reported as Ready.
- Always [backup your custom reports](backup-custom-reports.md) before upgrading!

---

## Version 16.0 June 23, 2025

# Version 16.0 (AppSource Version 1022)
**Release Date**: June 23, 2025
**App Source Version**: 1022

BI for SCCM Version 16.0, shown as version 1022 in AppSource, was released on June 23, 2025. This is a small maintenance release. Please see the full list below.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 16.0


### Product Enhancements

- N/A

### New Features

- N/A

### Bug Fixes

- In some cases the queries below are partially run to get the metadata even when the parameter is configured to disable them. This version introduced a fix to ensure those expensive queries are not run when parameters set to False.Application Deployment Status Enable
- Configuration Baseline Status Enable
- Software Update Deployment Status Enable
- Package Deployment Status Enable

### Semantic Model Changes

- N/A

### Important Notes

- Always [backup your custom reports](backup-custom-reports.md) before upgrading!

---

## Version 15.0 June 15, 2025

# Version 15.0 (AppSource Version 1021)
**Release Date**: June 11, 2025
**App Source Version**: 1021

BI for SCCM Version 15.0, shown as version 1021 in AppSource, was released on June 11, 2025. This is a small maintenance release primarily to fix two bugs affecting a limited number of customers. Please see the full list below.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 15.0


### Product Enhancements

- Updated “Chassis Type” definition to align with [Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-systemenclosure).

### New Features

- N/A

### Bug Fixes

- Resolved a bug which caused some environments experienced sync failures with the error message “There is already an object named '#LastLogonUser' in the database”.

### Semantic Model Changes

- N/A

### Important Notes

- Always [backup your custom reports](backup-custom-reports.md) before upgrading!

---

## Version 14.0 March 9, 2025

# Version 14.0 (AppSource Version 1020)
**BI for SCCM Version 14 (March 9, 2025)**

BI for SCCM Version 14.0, shown as version 1020 in AppSource, was released on March 9, 2025. This version brings many new features that have been requested by customers. Please see the full list below.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 14.0


**Product Enhancements:**

- N/A

**Semantic Model Changes:**

- Added new object "Maintenance Windows" to the data model. New fields include:New Fields "Description"
- "Duration (m)"
- "Is Enabled”
- "Is GMT"
- "Maintenance Window Count"
- "Maintenance Window Name"
- "Maintenance Window Type"
- "Recurrence Type"
- "Start Time"
Added new object "Software Asset Intelligence" to the data model. New fields include:
- "AI Category"
- "AI Family”
- "AI Publisher"
- "AI Software Name"
- "AI Tag"
- "AI Version"
Added new object "Software Asset Intelligence Tag" to the data model. New fields include:
- "AI Tag"
Update to the "Package Deployment Details" object in the data model. New field:
- "Adv ID"

**Bug Fixes:**

- N/A

**Important Notes:**

- Always backup your custom reports using our [backup process](backup-custom-reports.md).

---

## Version 13.0 Jan. 15, 2025

# Version 13.0 (AppSource Version 1019)
**BI for SCCM Version 13 (Jan. 14, 2025)**

BI for SCCM Version 13.0, shown as version 1019 in AppSource, was released on Jan. 14, 2025. This version brings many new features that have been requested by customers. Please see the full list below.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 13.0


**Product Enhancements:**

- Add new parameters to the semantic model to enable/disable features which have caused some customers timeout issues due to the size of the tables or the performance of SQL.Application Deployment Status Enable (Default: True)
- Configuration Baseline Status Enable (Default: True)
- Software Update Deployment Status Enable (Default: True)
- Package Deployment Status Enable (Default: True)

**Semantic Model Changes:**

- Added new object " Application Revisions " to the data model. New fields include:"Application Revisions Count",
- " Created By"
- "Date Created"
- "Date Created (Days)"
- "Is Latest"
- "Revision"

**Bug Fixes:**

- N/A

**Important Notes:**

- Always backup your custom reports using our [backup process](backup-custom-reports.md).

---

## Version 12.0 June 10, 2024

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

---
