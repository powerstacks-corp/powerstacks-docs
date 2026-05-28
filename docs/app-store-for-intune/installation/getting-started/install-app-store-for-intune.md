---
title: "Install App Store for Intune"
description: "What App Store for Intune is, what the install provisions, and the order of pages to follow for a fresh deployment."
---

# Install App Store for Intune

App Store for Intune is a full-lifecycle application management platform for Microsoft Intune environments. It deploys into your own Azure tenant — no vendor-hosted cloud, no shared credentials, no external processor of your data — and gives end users a branded self-service catalog where they can request the applications they need. Admins get a packaging pipeline that pulls WinGet-sourced installers, hash-verifies them, wraps them with PSADT v4, converts to `.intunewin`, and deploys through Intune's standard Win32 app pipeline. Custom MSI upload covers anything outside the WinGet catalog. Per-app approval workflows, Autopatch ring integration, version-rollback, programmatic API access, and Microsoft Teams notifications are included.

The install provisions an App Service, an Azure SQL database, a Key Vault, a storage account, an Application Insights workspace, and — when Teams notifications are enabled — an Azure Bot resource and a user-assigned managed identity for the bot. Database migrations apply on first start. After deploy, a one-time PowerShell snippet grants Microsoft Graph application permissions to the App Service's managed identity, and a first-run setup wizard inside the portal walks you through admin group selection, license activation, and the first Intune sync.

## Prerequisites

- An **Azure subscription** with Contributor permission on the target subscription or resource group.
- A **Microsoft Entra ID** Global Administrator or Application Administrator role, used to create the app registrations and to grant Microsoft Graph application permissions to the managed identity post-deploy.

## Setup steps in order

1. [Create the Entra app registration](../setup-guide/create-entra-app-registrations.md) — one registration that both validates incoming user tokens (exposing the `access_as_user` scope) and powers the SPA sign-in flow.
2. [Deploy to Azure](../setup-guide/deploy-to-azure.md) — run the custom-deployment wizard.
3. [Grant Microsoft Graph permissions to the App Service](../setup-guide/grant-graph-permissions.md) — one-time post-deploy PowerShell snippet that assigns the required Graph application roles to the App Service's managed identity.
4. [Add the production redirect URI](../setup-guide/add-redirect-uri.md) — add the App Service URL to the App Store app registration's SPA platform so sign-in succeeds.
5. [Sign in and verify](../setup-guide/sign-in.md) — confirm the portal is healthy and complete the in-portal Setup Wizard (admin group, license activation, first Intune sync).

## Optional post-deploy configuration

The portal is fully functional after step 5. The following are optional and can be configured at any time from the admin UI:

- [Configure email notifications](../setup-guide/configure-email-notifications.md)
- [Configure Microsoft Teams Bot](../setup-guide/configure-teams-bot.md)
- [Configure Application Insights](../setup-guide/configure-application-insights.md)
- [Configure a custom domain](../../administration/custom-domains.md)

For ongoing operations after install, see the [Admin Guide](../../administration/index.md).

## Next step

Continue to [Create Entra app registrations](../setup-guide/create-entra-app-registrations.md).
