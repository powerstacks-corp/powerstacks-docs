---
title: "Set up Windows Update for Business reports"
description: "Configure Windows Update for Business reports to populate Windows update compliance dashboards in BI for Intune."
---
# Set up Windows Update for Business reports

[Windows Update for Business reports](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview) is a Microsoft cloud service that surfaces Windows update compliance for Microsoft Entra joined devices. Microsoft routes the data into a Log Analytics workspace that you own; BI for Intune reads from that workspace to populate the WUfB Quality Updates, WUfB Feature Updates, WUfB Driver Updates, WUfB Delivery Optimization, and WUfB Windows Readiness dashboards.

This page walks through the recommended setup using Microsoft's Azure Workbook enrollment method.

!!! info "Last reviewed against Microsoft's docs: 2026-05-17"

## Step 1: Verify prerequisites

Before you start, confirm the following:

- An Azure subscription with Microsoft Entra ID.
- Devices are Microsoft Entra joined or Microsoft Entra Hybrid joined. (Entra registered alone is not supported.)
- Devices are running Windows 10 or Windows 11 — Pro, Education, Enterprise, or Enterprise multi-session editions.
- Devices have the February 2023 cumulative update or later.
- Devices send diagnostic data at the **Required** level or higher. Step 3 deploys an Intune configuration profile that sets this.
- The user enrolling has one of these roles: **Intune Administrator**, **Windows Update deployment administrator**, or **Policy and profile manager** (Intune RBAC role).
- The Log Analytics workspace must be in a [compatible Azure region](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites#log-analytics-regions). You create the workspace in Step 2.

Devices must also be able to reach Microsoft's required network endpoints. Most enterprise networks already allow these; for the full list see [Microsoft's prerequisites page](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites#endpoints).

## Step 2: Enable Windows Update for Business reports

Microsoft's recommended enrollment method is the Azure Workbook. It creates the Log Analytics workspace and enrolls the tenant into Windows Update for Business reports in a single flow.

1. Sign in to the [Azure portal](https://portal.azure.com).
1. In the search bar at the top, type **Monitor** and select **Monitor**.
1. In the Monitor left navigation, select **Workbooks**.
1. In the workbook gallery, select **Windows Update for Business reports**.
1. Select **Get started** to open the enrollment flyout.
1. Specify your **Subscription**.
1. For **Azure Log Analytics Workspace**, select **Create new workspace**, give it a name, and pick a supported region.
1. Select **Save settings** to enroll the tenant.

!!! tip "One workspace for both add-ons"
    If you also plan to set up [Custom Inventory](../custom-inventory.md), point it at this same workspace. BI for Intune reads both Windows Update for Business Reports data and Custom Inventory data from one Log Analytics workspace.

## Step 3: Deploy the Intune configuration profile to your devices

Windows Update for Business reports requires devices to send the diagnostic data the service relies on. The recommended way to configure this is a Settings catalog configuration profile in Intune.

1. Sign in to the [Intune admin center](https://intune.microsoft.com).
1. Go to **Devices** > **Windows** > **Configuration profiles**.
1. Select **Create profile**.
1. For **Platform**, choose **Windows 10 and later**. For **Profile type**, choose **Settings catalog**. Select **Create**.
1. On the **Basics** tab, enter a **Name** (for example, `WUfB reports — diagnostic data`) and an optional description.
1. On **Configuration settings**, select **Add settings** and search the **System** category. Add the following settings:

    | Setting | Value | Required? |
    |---|---|---|
    | Allow Telemetry | Basic | Required |
    | Configure Telemetry Opt In Settings Ux | Disabled | Recommended |
    | Configure Telemetry Opt In Change Notification | Disabled | Recommended |
    | Allow device name to be sent in Windows diagnostic data | Allowed | Recommended |

1. On **Assignments**, assign the profile to the device group you want reported on.
1. Select **Create** to save and assign the profile.

!!! tip "Set telemetry higher for complete data"
    **Basic** (renamed **Required**) is Microsoft's minimum requirement, but some data points in Windows Update for Business reports are only populated at higher diagnostic levels. For complete reporting, Microsoft recommends **Enhanced** for Windows 10 devices and **Optional** (previously **Full**) for Windows 11 devices.

Devices that are active and connected daily typically appear in Windows Update for Business reports within 72 hours. Less active devices may take up to two weeks.

## Step 4: Connect BI for Intune to the Log Analytics workspace

!!! note "May already be done"
    If you set up Custom Inventory before Windows Update for Business reports, this step may already be done. Check that the **AzureAD LogAnalytics WorkspaceID** parameter in your BI for Intune dataset matches the workspace from Step 2. If it does, skip to **What you'll see in BI for Intune** below.

1. In the Power BI service, open the **BI for Intune** workspace.
1. Open the BI for Intune **semantic model settings**.
1. Expand **Parameters** and update:
    - **AzureAD LogAnalytics Enable** = `TRUE`
    - **AzureAD LogAnalytics WorkspaceID** = the **Workspace ID** from Step 2. Find it at **Azure portal** > **Log Analytics workspaces** > your workspace > **Overview** > **Workspace ID**.
1. Select **Apply**.

## What you'll see in BI for Intune

After data starts flowing, the following BI for Intune dashboards populate:

- WUfB Quality Updates
- WUfB Feature Updates
- WUfB Driver Updates
- WUfB Delivery Optimization
- WUfB Windows Readiness

!!! info "Data takes up to 72 hours to appear"
    Devices that are active and connected daily typically appear in Windows Update for Business reports within 72 hours. Less active devices may take longer.

## Microsoft references

This page paraphrases content from Microsoft's official documentation. See Microsoft's docs for the canonical procedures:

- [Windows Update for Business reports overview](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview)
- [Prerequisites](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-prerequisites)
- [Enable Windows Update for Business reports](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-enable)
- [Configure devices via Intune](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-configuration-intune)
