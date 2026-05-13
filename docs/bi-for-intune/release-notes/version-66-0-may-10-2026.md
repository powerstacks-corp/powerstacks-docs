---
title: "Version 66.0 May 10, 2026"
render_macros: false
---

# Version 66

**Release Date:** May 10, 2026
**AppSource Version:** 1058

## Product Enhancements

- Updated handling for the Microsoft Intune Export API **DeviceInstallStatusByApp** endpoint to address intermittent synchronization failures caused by incomplete API responses.

## Bug Fixes

- Fixed an issue that could cause synchronization failures with the following error message: `We cannot convert the value null to type Text.. Microsoft.Data.Mashup.ErrorCode = 10277`
- Resolved a condition where the Microsoft Intune Export API returned a status of **Completed** while the export URL value was unexpectedly returned as null.
- Added additional validation logic to ensure a valid export URL is present before processing completed export jobs.

## Semantic Model Changes

- N/A

## Important Notes

- This issue was caused by unexpected behavior from a Microsoft Intune API response associated with application deployment status exports.
- Customers experiencing intermittent synchronization failures related to application deployment status data should update to this release as soon as possible.
- Always [back up your custom reports](../administration/backup-custom-reports.md) before upgrading.

## Summary

BI for Intune v66 hardens the application deployment status sync against a Microsoft Intune Export API edge case. When the **DeviceInstallStatusByApp** export occasionally completed with a null export URL, sync jobs would fail mid-run. The new validation logic catches the null URL case and the updated handling clears the error message customers were seeing (`Microsoft.Data.Mashup.ErrorCode = 10277`).

If you've seen intermittent sync failures on application deployment data, this release resolves them.
