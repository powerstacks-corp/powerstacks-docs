---
title: "Version 67.0 June 7, 2026"
render_macros: false
---

# Version 67

**Release Date:** June 7, 2026  
**AppSource Version:** 1059

## Product Enhancements

- Migrated **Compliance Policy State** and **Compliance Policy Setting State** data collection to the Microsoft Intune Export API to improve reliability and support larger datasets.
- Added a new relationship between the **Compliance Policy** and **Compliance Policy Setting** objects, allowing compliance settings to be viewed in the context of the policy that configured them.
- Updated the **Device Compliance Settings** page by adding **Policy Name** to the main table, filter pane, and drill-through pane.
- Updated the **Device Compliance** page by adding **Policy Name** to the drill-through pane.

## Semantic Model Changes

- Renamed semantic model parameter **AzureAD Export URL Wait (s)** to **AzureAD Export URL Post Wait (s)** (Default: 1 second). See the Important Notes section.
- Added new parameter **AzureAD Export URL Get Wait (s)** to the semantic model (Default: 1 second). This parameter controls the delay between Export API status checks during sync.
- Added new parameter **AzureAD Compliance Policy State Enable** to the semantic model (Default: True). This parameter controls whether Compliance Policy State data is collected during sync.

## Important Notes

- Renamed semantic model parameter **AzureAD Export URL Wait (s)** to **AzureAD Export URL Post Wait (s)**. This is a breaking change. Custom reports, documentation, or automation referencing the previous parameter name must be updated.
- Always [back up your custom reports](../administration/backup-custom-reports.md) before upgrading.

## Summary

BI for Intune v67 expands compliance reporting capabilities by introducing a relationship between **Compliance Policy** and **Compliance Policy Setting** data. This enhancement makes it easier to understand which settings are configured within a specific compliance policy and provides additional context when reviewing compliance configurations.

This release also enhances the **Device Compliance** and **Device Compliance Settings** pages with **Policy Name** filtering and drill-through capabilities, making it easier to analyze policy-specific compliance data.

In addition, compliance reporting data has been migrated to the Microsoft Export API and new semantic model parameters have been added to provide greater control over synchronization behavior and Compliance Policy State data collection.
