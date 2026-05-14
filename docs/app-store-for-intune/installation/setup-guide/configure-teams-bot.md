---
title: "Configure Microsoft Teams Bot"
description: "Optional. Send personal Teams Adaptive Card notifications via the bot the deploy template registered for you, plus the manual Teams admin center steps that still have to happen."
---

# Configure Microsoft Teams Bot

App Store for Intune can send personal Adaptive Card notifications in Teams to approvers and requestors. Each user receives their own notification — request submitted, approval needed, request approved, app installed.

The bot itself is the Azure Bot resource. If you set `enableTeamsBot=true` when you ran [Deploy to Azure](deploy-to-azure.md), the deploy template **already created the Azure Bot resource** and **already added the Teams channel**. What's left for you is the part the deploy template can't do for you: uploading the Teams app manifest to your Teams admin center, and then enabling notifications inside the portal.

## If you deployed via the Deploy to Azure button (recommended)

The bot is registered and the Teams channel is enabled. Skip straight to [Upload the Teams app manifest](#upload-the-teams-app-manifest).

## Manual bot registration (only if you deployed without `enableTeamsBot=true`)

Use this path only if you initially deployed with the bot disabled and want to add it later, or if your organization requires the bot to live in a separate resource group.

1. Navigate to **Azure Portal** > **Create a resource** > search for **Azure Bot**
2. Click **Create** and fill in:
    - **Bot handle**: a unique name (e.g., `AppRequestPortalBot`)
    - **Subscription / Resource group**: your existing App Store resource group is fine
    - **Pricing tier**: Free (F0) is sufficient
    - **Type of App**: Single Tenant
    - **Microsoft App ID**: select **Use existing app registration** and enter your **API client ID** (the same value you supplied as `apiClientId` to the deploy form)
3. After creation, open the Bot resource > **Configuration**
4. Set **Messaging endpoint** to: `https://<your-app-service-url>/api/messages`
5. In **Channels**, click **Microsoft Teams** > **Apply**

!!! note "Bot credentials"
    The bot shares the backend API's app registration — it does not need its own client ID or secret. The portal reads the bot credentials directly from `AzureAd__ClientId`, `AzureAd__ClientSecret`, and `AzureAd__TenantId`.

## Upload the Teams app manifest

For proactive messaging to work, the bot must be installed for each user. The repository ships a ready-to-use Teams app manifest in the `teams-bot-manifest/` folder.

1. Edit `teams-bot-manifest/manifest.json`. Replace `{{BOT_APP_ID}}` with your API client ID and update the URLs to point at your App Service.
2. Optionally replace the placeholder icons (`color.png`, `outline.png`) with your organization's branding.
3. Zip the three files (`manifest.json`, `color.png`, `outline.png`) into a single `.zip`.
4. Open **Teams Admin Center** > **Teams apps** > **Manage apps** > **Upload new app**, and upload the zip.
5. Go to **Teams apps** > **Setup policies** and edit **Global (Org-wide default)** — or create a custom policy targeted at the users who should receive notifications.
6. Under **Installed apps**, click **Add apps**, search for "App Store for Intune", and add it.
7. Click **Save**.

The bot is now scheduled to install for every user in scope. When it installs, it stores a conversation reference for that user, which is what makes proactive messaging work.

!!! note "Propagation time"
    Teams setup policies can take up to 24 hours to apply tenant-wide. Users can also install the bot manually from the Teams app store if they don't want to wait. Detailed manifest instructions are in `teams-bot-manifest/README.md` in the source repository.

## Enable notifications in the portal

1. Navigate to **Admin** > **Communications** tab
2. Under **Microsoft Teams Bot Notifications**:
    - Toggle **Enable Teams bot notifications** on
    - Enter the **Bot App ID** (your API client ID)
    - Click **Test** to send a test notification to yourself
    - Select which events should trigger notifications
3. Click **Save Settings**

## What gets notified

| Event | Recipient | Card Content |
|---|---|---|
| Approval Required | Approvers | Requestor, app name, publisher, justification, link to review |
| Request Approved | Requestor | App name, who approved, link to portal |
| Request Rejected | Requestor | App name, who rejected, rejection reason |
| App Installed | Requestor | App name, publisher, install timestamp |
| App Published | Admin/Creator | Package name, version, Intune App ID |

## Troubleshooting

- **Bot not sending messages** — the bot must be installed for the target user. Check the `BotConversationReferences` table in the database. If the user's entry is missing, the bot has never been installed for them.
- **401 Unauthorized on `/api/messages`** — the Azure Bot resource's Microsoft App ID doesn't match your API client ID, or the API app registration's client secret is expired. See [Rotate the API client secret](rotate-api-client-secret.md).
- **Test notification fails** — the bot must be installed for the testing user's account first. Check Teams Admin Center setup policies, or have the user install the bot manually.
- **Messages appear for some users but not others** — the setup policy hasn't propagated yet. Wait up to 24 hours, or have the users install the bot manually.

!!! note "Upgrading from v1.11.13 or earlier"
    Remove the four deprecated `Bot__` app settings (`Bot__MicrosoftAppId`, `Bot__MicrosoftAppPassword`, `Bot__MicrosoftAppType`, `Bot__MicrosoftAppTenantId`) from your App Service Configuration. If your Azure Bot resource was created with a different App ID than your API client ID, you need to delete and recreate the Bot resource with the correct App ID.

For detailed configuration, see the [Communications](../../administration/communications.md) admin guide page.

## Next step

Continue to [Configure Application Insights](configure-application-insights.md) (optional).
