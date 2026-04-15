---
title: "Version 18.0 April 5, 2026"
---
# Version 18.0 (AppSource Version 1024)
**Release Date**: April 5, 2026
**App Source Version**: 1024

BI for SCCM v18 is a small maintenance release that adds a single semantic model enhancement: support for the **XTS-AES 256 With Diffuser** encryption method. This addresses a gap in encryption data support that was introduced in v17.

**Important Notes:**
Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Please do not forget to [backup before you upgrade](backup-custom-reports.md)!


## Below Are the Changes in Version 18.0


### Semantic Model Changes

- Added **XTS-AES 256 With Diffuser** to the **Encryption Method** values on the **Computer Logical Disk** object.

### Important Notes

- Always [backup your custom reports](backup-custom-reports.md) before upgrading!
