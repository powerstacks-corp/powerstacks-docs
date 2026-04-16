---
title: "Version 16.0 June 23, 2025"
---
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
