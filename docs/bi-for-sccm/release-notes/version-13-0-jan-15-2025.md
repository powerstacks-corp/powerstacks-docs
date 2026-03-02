---
title: "Version 13.0 Jan. 15, 2025"
---
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
