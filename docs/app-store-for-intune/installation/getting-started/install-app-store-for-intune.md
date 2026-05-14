---
title: "Install App Store for Intune"
description: "Overview and prerequisites for installing App Store for Intune. The setup pages that follow walk through each step in order."
---

# Install App Store for Intune

App Store for Intune is a self-service portal that lets your users browse approved applications, request installs, and trigger Intune assignments without an admin ticket. Installing it sets up the API, web portal, database, and the Entra ID app registrations needed to connect to Microsoft Graph.

This guide walks you through setting up App Store for Intune from scratch.

## Prerequisites

- Azure subscription with appropriate permissions
- Entra ID tenant with Global Administrator or Application Administrator role
- .NET 8.0 SDK
- Node.js 18+ and npm
- Visual Studio 2022 or VS Code
- Azure CLI installed
- SQL Server (LocalDB, Express, or Developer Edition) or Azure SQL Database

### Install required .NET tools

Install the Entity Framework Core CLI tools:

```powershell
# Add NuGet source if not already configured
dotnet nuget add source https://api.nuget.org/v3/index.json -n nuget.org

# Install EF Core tools globally
dotnet tool install --global dotnet-ef
```

## What the setup pages cover

The sub-pages in this section walk through the install in order:

1. [Create Entra App Registrations](../setup-guide/create-entra-app-registrations.md) — the backend API and the frontend SPA
2. [Configure Application Settings](../setup-guide/configure-application-settings.md) — wire the API and web project to your tenant
3. [Database Setup](../setup-guide/database-setup.md) — connection string and EF Core migrations
4. [Configure Admin Access](../setup-guide/configure-admin-access.md) — required; the portal fails closed until this is set
5. [Deploy to Azure](../setup-guide/deploy-to-azure.md) — ARM template deployment and troubleshooting
6. [Configure Email Notifications](../setup-guide/configure-email-notifications.md) — optional
7. [Configure Microsoft Teams Bot](../setup-guide/configure-teams-bot.md) — optional
8. [Configure Application Insights](../setup-guide/configure-application-insights.md) — optional

Configure your approval workflows once the portal is running, see [Approval Workflows](../../administration/approval-workflows.md).

## Next step

Start with [Create Entra App Registrations](../setup-guide/create-entra-app-registrations.md).
