---
title: "Install App Store for Intune"
description: "What you need before installing App Store for Intune, what the Deploy to Azure button does for you, and what you still do by hand."
---

# Install App Store for Intune

App Store for Intune is a self-service application portal that runs entirely inside your Azure tenant. The fastest way to install it is the **Deploy to Azure** button: one ARM template provisions the App Service, the Azure SQL Database, the Key Vault, the storage account, the (optional) Azure Bot resource, and the networking between them. Migrations apply on first start. There is no separate database setup step, no manual configuration of app settings, and no developer tooling to install.

The only things you do by hand are the two Entra ID app registrations (the API and the SPA), creating two security groups (admins and approvers), and clicking the button.

## Prerequisites

- An **Azure subscription** with permission to create resource groups and resources (Contributor on the target subscription or resource group).
- **Microsoft Entra ID** Global Administrator or Application Administrator role, used to create the two app registrations and grant the Graph API permissions the portal needs.

That's it. You do not need .NET, Node.js, Visual Studio, the Azure CLI, NuGet, or the EF Core CLI to install the product. Those are only useful if you're building from source.

You do not need a local SQL Server. Azure SQL is provisioned by the deploy template.

## Setup steps in order

1. [Create Entra App Registrations](../setup-guide/create-entra-app-registrations.md) — two registrations: the backend API (with Microsoft Graph application permissions and a client secret you'll paste into the deploy form) and the frontend SPA (client ID only).
2. [Configure Admin Access](../setup-guide/configure-admin-access.md) — create the admin and approver security groups in Entra ID and copy their Object IDs. The portal fails closed until an admin group is set, so this is required, not optional.
3. [Deploy to Azure](../setup-guide/deploy-to-azure.md) — click the button, fill the parameter form, wait 10-15 minutes. This is the install.
4. [Configure Email Notifications](../setup-guide/configure-email-notifications.md) — optional. Email notifications for approvers and requestors.
5. [Configure Microsoft Teams Bot](../setup-guide/configure-teams-bot.md) — optional. If you set `enableTeamsBot=true` in step 3, the Azure Bot resource is already registered for you; this page covers the Teams app manifest upload that still has to happen in the Teams admin center.
6. [Configure Application Insights](../setup-guide/configure-application-insights.md) — optional. Application logging and telemetry.

After the deploy completes, the [Admin Guide](../../administration/index.md) is where the ongoing configuration lives — portal settings, approval workflows, the app catalog, PSADT configuration via Intune ADMX, and so on.

## Next step

Start with [Create Entra App Registrations](../setup-guide/create-entra-app-registrations.md).
