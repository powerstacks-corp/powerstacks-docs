---
title: "Version 63.0 Jan. 8, 2026"
render_macros: false
---

# Version 63

**Release Date:** January 8, 2026
**AppSource Version:** 1055

## New Features

- Added Endpoint Security **Configuration Policy** types to the data model. Policy types include:
    - **App and Browser Isolation**
    - **App Control for Business**
    - **BitLocker**
    - **Microsoft Defender Antivirus**
    - **Endpoint Detection and Response**
    - **Windows Firewall**
    - **macOS FileVault**

## Semantic Model Changes

- Extended the data model to include Endpoint Security **Configuration Policy** objects.

## Important Notes

- Microsoft Graph API instability (HTTP 503 / 504) continues to affect some tenants intermittently. The **AzureAD Application Assignment Enable** parameter (added in v61) provides a temporary workaround. Please contact us if you encounter this — additional support cases opened with Microsoft will help prioritize a fix.
- Several customers have recently reported upgrade failures resulting in the loss of their custom reports. Always [back up your custom reports](../administration/backup-custom-reports.md) before upgrading.

## Summary

BI for Intune v63 brings additional **Configuration Policy** type data into the semantic model, covering Endpoint Security policy types such as App and Browser Isolation, App Control for Business, BitLocker, Microsoft Defender Antivirus, Endpoint Detection and Response, Windows Firewall, and macOS FileVault.
