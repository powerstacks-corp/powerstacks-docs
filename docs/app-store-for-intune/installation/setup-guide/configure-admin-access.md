---
title: "Configure Admin Access"
description: "Required. Create the admin and approver security groups in Entra ID and copy their Object IDs into the Deploy to Azure form. The portal fails closed until an admin group is set."
---

# Configure Admin Access

App Store for Intune fails closed. Until you provide an admin group, **every admin endpoint returns 403** — including for the person who deployed it. There is no first-run setup wizard. So you create the groups before deploy and paste their Object IDs into the deploy form.

You will create two groups: one for administrators (full access, can sync apps from Intune, configure settings, manage approvals) and one for approvers (can approve and reject app requests). You can use the same group for both if you don't need a separation of duties.

## Create the admin security group

1. Navigate to **Azure Portal** > **Microsoft Entra ID** > **Groups**
2. Click **New group**
3. Settings:
    - Group type: **Security**
    - Group name: `AppStore-Admins` (or your preferred name)
    - Group description: `Administrators for App Store for Intune`
    - Membership type: **Assigned**
4. Click **Create**
5. Open the new group and add the users who should have admin access
6. Copy the **Object ID** from the group's **Overview** page — you'll paste it into the Deploy to Azure form as `adminGroupId`.

## Create the approver security group

Repeat the same flow with the name `AppStore-Approvers`. Add the users who should be able to approve and reject app requests. Copy the **Object ID** — you'll paste it as `approverGroupId`.

You can skip this step and pass the admin group's Object ID for both parameters if you don't need separate approver permissions.

## What happens after deploy

The deploy template writes these Object IDs to the App Service configuration (`AppSettings__AdminGroupId` and `AppSettings__ApproverGroupId`). The portal seeds them into its database on first start, so the values become editable from the admin UI without redeploying.

After install, the recommended way to change either group is through the portal:

1. Sign in as a member of the admin group
2. Navigate to **Admin** > **Settings** tab
3. Under **Group-Based Authorization**, update the Object IDs and click **Save Settings**

The portal reads database values first and falls back to the App Service configuration values. Keeping the App Service values in place provides a recovery path if the database settings are accidentally cleared.

## Next step

Continue to [Deploy to Azure](deploy-to-azure.md) — the install itself.
