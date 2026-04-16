---
title: "Version 17.0 February 20, 2026"
---
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
