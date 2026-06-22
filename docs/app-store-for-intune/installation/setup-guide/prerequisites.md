---
title: "Prerequisites"
description: "Roles, quota, and resources to confirm before installing App Store for Intune from the Azure Marketplace."
---

# Prerequisites

Confirm all of the following before you install App Store for Intune.

## Roles you need to install

Sign in to the Azure portal with an account that has:

- **Microsoft Entra ID**: Global Administrator, or Privileged Role Administrator together with Cloud Application Administrator. Cloud Application Administrator creates the app registration. Privileged Role Administrator (or Global Administrator) grants the Microsoft Graph permissions to the App Service's managed identity in the post-deploy step.
- **Azure**: Owner on the subscription where you install App Store for Intune. Owner is required because the deployment creates role assignments, which Contributor cannot do.

## Subscription and region

The subscription must support deploying Azure SQL, App Service, Key Vault, Application Insights, and Storage, plus an Azure Bot if you enable Teams notifications, in the Azure region you select during deployment.

## App Service quota

App Store for Intune runs on a single App Service Plan. Before you deploy, open **App Service plan quota** for your target subscription and region in the Azure portal and confirm you have capacity for the plan size and instance count you'll choose. The defaults are **B2** and **1 instance**, which is **1 x B2** for a standard install.

If you don't have enough quota, raise a Microsoft support request to increase the App Service quota in that subscription and region.

## What the install deploys

- App Service and App Service Plan. The App Service's system-assigned managed identity is the runtime identity for Microsoft Graph calls.
- Azure SQL Server and the App Store database.
- Key Vault, holding the SQL and storage connection strings.
- Storage account, used by the packaging pipeline.
- Application Insights.
- Azure Bot and a user-assigned managed identity, only when Teams notifications are enabled.

For the full picture, see [Architecture overview](../../administration/architecture.md).

## Outbound network access

Standard deployments need no network configuration. If you restrict outbound traffic with VNet integration or a firewall, allow the App Service to reach:

- `login.microsoftonline.com`: sign-in
- `graph.microsoft.com`: Intune management through Microsoft Graph
- `bi.powerstacks.com`: the application package host
- Your Azure SQL, Key Vault, Storage, and Application Insights endpoints

## Next step

Continue to [Create the Entra app registration](create-entra-app-registrations.md).
