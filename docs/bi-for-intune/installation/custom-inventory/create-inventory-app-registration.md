---
title: "Create Entra Application"
render_macros: false
---

# Create Entra Application for Enhanced Inventory

Enhanced Inventory uses an Entra application to authenticate to Azure and send inventory data via the Log Ingestion API. This page walks through creating the application and recording the credentials needed for deployment.

!!! warning "Enterprise Application, not App Registration"
    You must create an **Enterprise Application** first, not a standard App Registration. The ARM deployment template requires the **Enterprise Application Object ID** (the service principal Object ID), which is different from the App Registration Object ID.

## Prerequisites

**Microsoft Entra permissions required:**

- **Application Administrator** or **Global Administrator**

**Azure permissions required (for the deployment in the next step):**

- **Contributor** or **Owner** on the target subscription or resource group
- **User Access Administrator** or **Owner** to assign roles (only required if you want automatic RBAC assignment)

## Step 1: Create the Enterprise Application

1. In the [Azure Portal](https://portal.azure.com), navigate to **Microsoft Entra ID** > **Enterprise applications**.
2. Select **New application** > **Create your own application**.
3. Enter a name (e.g., `PowerStacks-EnhancedInventory`).
4. Select **Integrate any other application you don't find in the gallery**.
5. Click **Create**.
6. From the Enterprise Application overview page, record the **Object ID**.

!!! tip "Why Enterprise Application?"
    We create it as an Enterprise Application because the Object ID shown there is what the ARM template needs for the `Ingestion Sp Object Id` parameter. The App Registrations blade shows a *different* Object ID that will not work.

## Step 2: Get credentials from App Registrations

After creating the Enterprise Application, switch to the **App Registrations** blade to get the credentials the inventory scripts will use:

1. Navigate to **Microsoft Entra ID** > **App registrations**.
2. Find the application you just created (search by name).
3. From the **Overview** page, record:
    - **Directory (Tenant) ID**
    - **Application (Client) ID**
4. Navigate to **Certificates & secrets** > **New client secret**.
5. Enter a description and select an expiration period.
6. Click **Add** and immediately record the **Value** (not the Secret ID). The value is only shown once.

## Values to record

By the end of this step, you should have:

| Value | Where to find it | Used by |
| --- | --- | --- |
| **Enterprise App Object ID** | Enterprise Applications > Overview | ARM deployment template |
| **Directory (Tenant) ID** | App Registrations > Overview | Inventory scripts |
| **Application (Client) ID** | App Registrations > Overview | Inventory scripts |
| **Client Secret Value** | App Registrations > Certificates & secrets | Inventory scripts |

## Next step

[Deploy Azure Resources](deploy-custom-inventory-resources.md) — use the Deploy to Azure button to create your Log Analytics workspace, custom tables, DCE, and DCR.
