---
title: "Version 61.0 Oct. 28, 2025"
render_macros: false
---

# Version 61

**Release Date:** October 28, 2025
**AppSource Version:** 1053

## Product Enhancements

- Added a retry function for all API calls that use redirects, improving reliability in unstable network conditions.
- Updated the **Device Timeline Event** parameter — the default value is now **-1 (Disabled)** instead of **7 days**, to prevent unnecessary calls for customers not using Intune Advanced Analytics.
- Updated the [**Custom Inventory for Windows**](https://github.com/powerstacks-corp/Windows-Custom-Inventory) script to resolve a bug in the driver matching process.

## New Features

- Added a new parameter **AzureAD Application Assignment Enable** _(default: **TRUE**)_ that lets you disable **Application Assignment** data collection in environments where the Microsoft Graph API intermittently returns HTTP 503 or 504 errors.

## Bug Fixes

- Resolved an issue in **Autopilot Enrollment** where some Autopilot devices were missing their assigned profiles.
- Resolved timeouts triggered by the **AzureAD Group Members Filter Starts With** and **AzureAD Group Members Nested Crawler Enable** parameters.

## Semantic Model Changes

- Updated the **Compliance State Device** object — removed summarization on **Update Installed Time (Days)** and **Update Release Time (Days)** for more granular reporting.
- Updated the **Authorization** object to include a new **Viewer Email** field.
- Renamed object **User Proxy Addresses** to **User Proxy Address** for naming consistency.

## Important Notes

- [**Action Required**] If you have existing custom reports referencing the renamed **User Proxy Addresses** object, you must update them to use **User Proxy Address**.
- Microsoft Graph API instability (HTTP 503 / 504) continues to affect some tenants intermittently. The new **AzureAD Application Assignment Enable** parameter provides a temporary workaround. Please contact us if you encounter this — additional support cases opened with Microsoft will help prioritize a fix.
- Always [back up your custom reports](../administration/backup-custom-reports.md) before upgrading.

## Summary

BI for Intune v61 focuses on stability and synchronization performance. Highlights include retry handling for redirected API calls, a new parameter to work around Microsoft Graph 503 / 504 errors, fixes for Autopilot enrollment and group-member sync timeouts, and a refreshed Custom Inventory for Windows script.
