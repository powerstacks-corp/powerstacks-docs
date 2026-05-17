---
title: "Configure Email Notifications"
description: "Optional. Enable email notifications for request submissions, approvals, and rejections by adding Mail.Send permission and a sender mailbox."
---

# Configure Email Notifications

The portal can send email notifications for:

- Request submitted confirmations
- Approval required notifications to approvers
- Request approved/rejected notifications to requestors

## Prerequisites

1. **Mail.Send permission** must be added to your API app registration (see [Create Entra app registrations](create-entra-app-registrations.md), item 8).
2. A **user mailbox or shared mailbox** to send emails from.

## Add Mail.Send permission

If you didn't add it during initial setup:

1. Go to **Azure Portal** > **Microsoft Entra ID** > **App registrations**.
2. Select your **backend API** app registration.
3. Select **API permissions** > **Add a permission**.
4. Select **Microsoft Graph** > **Application permissions**.
5. Search for `Mail.Send` and check it.
6. Select **Add permissions**.
7. Select **Grant admin consent for [your tenant]** (requires Global Administrator or Privileged Role Administrator).

## Get the user object ID

You need the Object ID of the user or shared mailbox that will send emails:

1. Go to **Azure Portal** > **Microsoft Entra ID** > **Users**.
2. Search for and select the user (or shared mailbox).
3. Copy the **Object ID** from the Overview page.

!!! tip
    You can create a dedicated shared mailbox like `apprequest-noreply@yourdomain.com` for this purpose.

## Option A: configure via portal settings UI (recommended)

1. Go to **Admin** > **Communications** tab.
2. Under **Email Notifications**:
   - Toggle **Enable email notifications** on.
   - Enter the **Send As User ID** (Object ID of mailbox).
   - Enter the **From Address** (email address).
   - Enter the **Portal URL** (for email links).
3. Select **Save Settings**.

## Option B: configure via appsettings.json

Update `appsettings.json`:

```json
{
  "EmailSettings": {
    "SendAsUserId": "user-object-id-here",
    "FromAddress": "apprequest-noreply@yourdomain.com",
    "PortalUrl": "https://your-portal-url.com"
  }
}
```

| Setting | Description |
|---------|-------------|
| `SendAsUserId` | The Object ID of the user or shared mailbox to send emails from. If empty, email notifications are disabled. |
| `FromAddress` | The email address shown in the From field (should match the mailbox). |
| `PortalUrl` | The URL of your portal, used for links in email notifications. |

!!! tip
    Settings configured in the UI take precedence over `appsettings.json` values.

## Test email notifications

1. Submit an app request.
2. Check that the requestor receives a confirmation email.
3. Check that approvers receive an approval request email.
4. Approve or reject the request and verify the requestor receives the result notification.

## Troubleshooting email issues

- **403 Forbidden**: Ensure `Mail.Send` permission has admin consent granted.
- **User not found**: Verify the `SendAsUserId` is a valid Object ID.
- **Email not sent**: Check the API logs for detailed error messages.

## Next step

Continue to [Configure Microsoft Teams Bot](configure-teams-bot.md) (optional).
