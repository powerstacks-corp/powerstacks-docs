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

1. Create a **user-assigned managed identity** in your App Store resource group (Azure Portal > **Create a resource** > **User Assigned Managed Identity**). Name it something like `uami-bot-apprequest`. Note its **Client ID** and **Resource ID** from the Overview blade.
2. Attach the UAMI to your App Service: App Service > **Identity** > **User assigned** tab > **Add** > select the UAMI you just created.
3. Add a new app setting on the App Service called `Bot__UamiClientId` set to the UAMI's Client ID, then restart the App Service.
4. Navigate to **Azure Portal** > **Create a resource** > search for **Azure Bot**.
5. Click **Create** and fill in:
    - **Bot handle**: a unique name (e.g., `AppRequestPortalBot`)
    - **Subscription / Resource group**: your existing App Store resource group is fine
    - **Pricing tier**: Free (F0) is sufficient
    - **Type of App**: **User-Assigned Managed Identity**
    - **App Service Microsoft App ID**: the UAMI's Client ID
    - **Tenant ID**: your Entra tenant ID
    - **User-Assigned Managed Identity**: pick the UAMI you created in step 1
6. After creation, open the Bot resource > **Configuration**.
7. Set **Messaging endpoint** to: `https://<your-app-service-url>/api/messages`.
8. In **Channels**, click **Microsoft Teams** > **Apply**.

!!! note "Why a UAMI, not the API app registration"
    Earlier releases of App Store for Intune used the backend API's app registration and a client secret for the bot's outbound calls to the Bot Connector. As of v1.30.0, the bot uses a dedicated user-assigned managed identity instead — no client secret involved. The deploy template provisions and wires this up automatically when `enableTeamsBot=true`; this manual flow only matters if you skip that and add the bot later.

## Upload the Teams app manifest

For proactive messaging to work, the bot must be installed for each user. The repository ships a ready-to-use Teams app manifest in the `teams-bot-manifest/` folder.

1. Edit `teams-bot-manifest/manifest.json`. Replace `{{BOT_APP_ID}}` with the **Bot UAMI Client ID** (visible in the deploy outputs as `teamsBotAppId`, or on the user-assigned managed identity resource's Overview blade) and update the URLs to point at your App Service.
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
    - Enter the **Bot App ID** (the Bot UAMI's Client ID — visible in the deploy outputs as `teamsBotAppId`)
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
- **401 Unauthorized on `/api/messages`** — the Azure Bot resource's MSI configuration doesn't match the UAMI attached to the App Service. Check that the Bot resource's **Microsoft App ID** matches the **Client ID** of the UAMI assigned to the App Service, and that the same UAMI is attached to the App Service in **Identity** > **User assigned**.
- **Test notification fails** — the bot must be installed for the testing user's account first. Check Teams Admin Center setup policies, or have the user install the bot manually.
- **Messages appear for some users but not others** — the setup policy hasn't propagated yet. Wait up to 24 hours, or have the users install the bot manually.

For detailed configuration, see the [Communications](../../administration/communications.md) admin guide page.

## Next step

Continue to [Configure Application Insights](configure-application-insights.md) (optional).
