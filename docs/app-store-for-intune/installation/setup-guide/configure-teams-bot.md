---
title: "Configure Microsoft Teams Bot"
description: "Optional. Send personal Teams Adaptive Card notifications to approvers and requestors using Bot Framework proactive messaging."
---

# Configure Microsoft Teams Bot

Send personal Teams notifications to approvers and requestors via a Teams Bot using Bot Framework proactive messaging. Each user receives individual Adaptive Card notifications in their Teams chat.

The bot uses the same app registration as the API. No separate `Bot__` environment variables are needed. Credentials are read directly from `AzureAd__ClientId`, `AzureAd__ClientSecret`, and `AzureAd__TenantId`.

> **ARM Template Deployment:** If you used the "Deploy to Azure" button, the ARM template automatically created the Azure Bot resource and enabled the Teams channel. You can skip steps 1 and 2 below and go directly to [Pre-install the bot for users](#pre-install-the-bot-for-users).

## Register an Azure Bot

1. Navigate to **Azure Portal** > **Create a resource** > search for **Azure Bot**
2. Click **Create** and fill in:
   - **Bot handle**: A unique name (e.g., `AppRequestPortalBot`)
   - **Subscription/Resource Group**: Use your existing resource group
   - **Pricing tier**: Free (F0) is sufficient
   - **Type of App**: Single Tenant
   - **Microsoft App ID**: Select **Use existing app registration** and enter your **API Client ID** (the same `AzureAd__ClientId` from [Create Entra App Registrations](create-entra-app-registrations.md))
3. After creation, go to the Bot resource > **Configuration**
4. Set **Messaging endpoint** to: `https://your-app-url/api/messages`

## Add the Teams channel

1. In the Azure Bot resource, go to **Channels**
2. Click **Microsoft Teams** > **Apply**
3. This enables the bot to communicate through Teams

## Pre-install the bot for users

For proactive messaging to work, the bot must be installed for each user. A ready-to-use Teams app manifest is included in the `teams-bot-manifest/` directory.

1. Edit `teams-bot-manifest/manifest.json`. Replace `{{BOT_APP_ID}}` with your API Client ID and update the URLs
2. Optionally replace the placeholder icons (`color.png`, `outline.png`) with your organization's branding
3. Zip the three files (`manifest.json`, `color.png`, `outline.png`) into a `.zip` file
4. In **Teams Admin Center** > **Teams apps** > **Manage apps** > **Upload new app**, upload the zip
5. Go to **Teams apps** > **Setup policies** > edit **Global (Org-wide default)** (or create a custom policy)
6. Under **Installed apps**, click **Add apps**, search for "App Store for Intune", and add it
7. Click **Save**. The bot will be automatically installed for all users in scope

> **Note:** It may take up to 24 hours for the policy to apply to all users. When the bot is installed for a user, it automatically stores a conversation reference that enables proactive messaging. See `teams-bot-manifest/README.md` for detailed instructions.

## Configure in portal

1. Navigate to **Admin** > **Communications** tab
2. Under **Microsoft Teams Bot Notifications**:
   - Toggle **Enable Teams bot notifications** on
   - Enter the **Bot App ID** (your API Client ID from [Create Entra App Registrations](create-entra-app-registrations.md))
   - Click **Test** to send a test notification to yourself
   - Select which events should trigger notifications
3. Click **Save Settings**

## What gets notified

| Event | Recipient | Card Content |
|-------|-----------|-------------|
| **Approval Required** | Approvers | Requestor, app name, publisher, justification, link to review |
| **Request Approved** | Requestor | App name, who approved, link to portal |
| **Request Rejected** | Requestor | App name, who rejected, rejection reason |
| **App Installed** | Requestor | App name, publisher, install timestamp |
| **App Published** | Admin/Creator | Package name, version, Intune App ID |

## Troubleshooting Teams bot issues

- **Bot not sending messages**: Ensure the bot is installed for the target user (check `BotConversationReferences` table in the database)
- **401 Unauthorized on /api/messages**: Verify the Azure Bot resource's Microsoft App ID matches your `AzureAd__ClientId`, and that the app registration has a valid client secret
- **Test notification fails**: The bot must be installed for your user account first. Check Teams Admin Center setup policies
- **Messages not appearing for some users**: The setup policy may not have propagated yet (up to 24 hours). Users can also manually install the bot from the Teams app store

> **Upgrading from v1.11.13 or earlier:** Remove the 4 deprecated `Bot__` environment variables (`Bot__MicrosoftAppId`, `Bot__MicrosoftAppPassword`, `Bot__MicrosoftAppType`, `Bot__MicrosoftAppTenantId`) from your App Service. If your Azure Bot resource was created with a different App ID than your API Client ID, you must delete and recreate it with the correct App ID.

For detailed configuration instructions, see the [Admin Guide](../../administration/).

## Next step

Continue to [Configure Application Insights](configure-application-insights.md) (optional).
