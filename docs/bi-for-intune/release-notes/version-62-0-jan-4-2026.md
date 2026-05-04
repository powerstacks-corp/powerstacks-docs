---
title: "Version 62.0 Jan. 4, 2026"
render_macros: false
---

# Version 62

**Release Date:** January 4, 2026
**AppSource Version:** 1054

## Product Enhancements

- Windows devices managed by **MAM-WE** now display a friendly **Device Type** of **Windows** instead of **1**.

## New Features

- Added a new data source: **Windows Distribution Report**.
- Added new fields to the **Device** category, sourced from **Windows Distribution Report**:
    - Device Tag
    - OS Build Number
    - OS Build Revision
    - OS Quality Update Release Date
    - OS Quality Update Release Date (Months)
    - OS Quality Update Type
    - OS Quality Update Version
    - WU Distribution Enrolled
- **OS Release ID** in the **Device** category is now populated by **Windows Distribution Report** data.
- Added a new **Device Tag** category to the model with a new **Tag** field. _(Populated only for Windows devices.)_
- Updated the **Device Info** page with new fields: **OS Quality Update Version**, **OS Quality Update Release Date**, and **OS Quality Update Type**.

## Semantic Model Changes

- Added new **Device** fields sourced from the **Windows Distribution Report**: Device Tag, OS Build Number, OS Build Revision, OS Quality Update Release Date, OS Quality Update Release Date (Months), OS Quality Update Type, OS Quality Update Version, WU Distribution Enrolled.
- Repointed **OS Release ID** in the **Device** category to the **Windows Distribution Report** source.
- Added a new **Device Tag** category with the **Tag** field. _(Populated only for Windows devices.)_

## Important Notes

- Microsoft Graph API instability (HTTP 503 / 504) continues to affect some tenants intermittently. The **AzureAD Application Assignment Enable** parameter (added in v61) provides a temporary workaround. Please contact us if you encounter this — additional support cases opened with Microsoft will help prioritize a fix.
- Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Always [back up your custom reports](../administration/backup-custom-reports.md) before upgrading.

## Summary

BI for Intune v62 adds the **Windows Distribution Report** data source, providing greater detail about installed Windows versions, including build number, build revision, quality update version and release date, and a new device-tag category for Windows devices.
