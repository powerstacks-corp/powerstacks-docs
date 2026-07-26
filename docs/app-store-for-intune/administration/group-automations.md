---
title: "Group automations"
description: "Keep a Microsoft Entra ID device group in sync with the devices that have a given app installed, refreshed daily from BI for Intune."
---

# Group automations

Group Automations keeps a Microsoft Entra ID device group in sync with the devices that have a given app installed. Membership is refreshed once a day from BI for Intune, so you can target an app update or ring deployment at just the devices that need it instead of targeting everyone.

!!! tip "Best practice: reuse a group for update deployments"
    Point an App Update or ring deployment at the Entra device group an automation manages. Only the devices that actually have the app receive the update, and the membership stays current without manual edits.

## Connecting BI for Intune

Group Automations reads installed-app data from your BI for Intune semantic model. The App Store connects to it as its managed identity (no secret) and runs read-only queries.

Under **Settings**, in the **BI for Intune connection** section, provide the Power BI **workspace ID** and **semantic model (dataset) ID**, then select **Test connection** to confirm access before you create an automation.

### Requirements

- BI for Intune with populated app inventory on a Power BI Pro (or higher) workspace.
- The App Store managed identity added to that workspace with **Build** permission.
- The Power BI tenant settings **Service principals can use Fabric APIs** and **Semantic Model Execute Queries REST API** enabled for the App Store managed identity. A Fabric (Power BI) administrator sets these once in the Power BI admin portal, scoped to the whole organization or to a Microsoft Entra ID security group that contains the managed identity.

!!! note
    Tenant-setting changes can take up to 15 minutes to take effect.

!!! warning
    The App Store managed identity also needs the Microsoft Graph **Device.Read.All** (or **Directory.Read.All**) application permission. Membership sync matches a device in BI for Intune, then resolves it to its Entra ID device object before adding it to the group. Without this permission, a run reports matched devices but adds none.

## Creating an automation

Go to **Automations** > **Group Automations** and select **New automation**. Then define:

- **Name**: a name for the automation, and an optional description.
- **Target Entra group**: create a new device security group, or select an existing one. The group name is required. The App Store manages the group's membership, so avoid editing it by hand.
- **Membership rule**: include a device when its installed apps match **all** or **any** of a set of conditions. Each condition is on **Application name**, **Publisher**, or **Version**.
- **Options**: remove devices that no longer match, notify on membership changes, and enable or disable the automation.

Select **Preview matching devices** to see how many devices match, listed by device name, before you save.

!!! tip "Matching apps that put the version in the name"
    For an app such as Oracle Java that includes its version in the display name, match the product line with **Application name starts with** and compare separately on **Version**.

## How the daily run works

All enabled automations reconcile once a day, tenant-wide, one automation at a time.

Reconciliation adds and removes only the difference between the current group and the matched devices. It never rebuilds the group from scratch. A run that matches zero devices, or that fails to query, is skipped and the group is left intact, so a temporary data problem cannot empty a group.

Membership updates only the group. You still target the update itself from **App Management** by pointing an App Update or ring deployment at the group.

## Notifications

Turn on notifications under **Communications** for:

- Membership changes.
- Failed or skipped runs.
- Configuration changes.

Notifications are delivered over the email and Teams channels configured on the **Communications** tab.
