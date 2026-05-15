---
title: "Sign in and verify"
description: "Verify the portal is healthy, sign in for the first time, and complete the in-portal Setup Wizard."
---

# Sign in and verify

The portal is deployed, the App Service has its Graph permissions, and the frontend app registration has the production redirect URI. This page walks through the first sign-in and the in-portal Setup Wizard that finishes configuration.

## Verify the portal is healthy

Open these two URLs in a browser. Replace `<sitename>` with your App Service name.

- `https://<sitename>.azurewebsites.net/health` — returns `200 OK` when the portal is running and the Key Vault references resolve.
- `https://<sitename>.azurewebsites.net/health/migrations` — returns `"pendingCount": 0` when all database migrations have applied.

If either endpoint reports an error, see [Troubleshooting](troubleshooting.md).

## First sign-in

1. Open `https://<sitename>.azurewebsites.net/` in a browser.
2. Sign in with an Entra ID account that has the **Microsoft Entra ID Global Administrator** or **Application Administrator** role. The portal grants this account temporary admin access on first run so it can complete the Setup Wizard.

## Complete the Setup Wizard

On first sign-in the portal opens the **Setup Wizard**, which walks through the remaining configuration. The wizard has four steps:

1. **Activate your license.** Enter the license key supplied by PowerStacks. The wizard validates the key against the licensing service and displays the expiration date and enabled features.
2. **Choose your admin security group.** Search Entra ID for an existing group, or create a new one directly from the wizard. Members of this group gain admin access to the portal. The signed-in user is added to the new group automatically when you create one from the wizard.
3. **Configure email notifications.** Optional. Select an Entra ID user mailbox to send notifications from, and enter the From address that recipients will see. You can skip this step and configure email later from **Admin** > **Communications**.
4. **Run the first Intune sync.** Pulls the existing Intune app catalog into the portal so the admin App Catalog tab is populated immediately. This typically takes 30 to 60 seconds depending on catalog size.

Select **Finish**. The wizard saves the settings to the database and routes you to the admin dashboard.

## What "done" looks like

After **Finish**, the admin dashboard loads. **Admin** > **App Catalog** shows the apps synced from Intune. **Admin** > **Settings** > **Group-Based Authorization** shows the admin group you selected. The portal is fully operational.

## Next step

The install is complete. Continue with optional configuration as needed:

- [Configure email notifications](configure-email-notifications.md) — if you skipped this step in the wizard or want to refine the settings.
- [Configure Microsoft Teams Bot](configure-teams-bot.md) — finish the Teams app manifest upload if you enabled the bot at deploy time.
- [Configure Application Insights](configure-application-insights.md) — application logging and telemetry.
- [Custom domains](../../administration/custom-domains.md) — replace the default `*.azurewebsites.net` URL with a custom domain.

For ongoing administration, see the [Admin Guide](../../administration/index.md).
