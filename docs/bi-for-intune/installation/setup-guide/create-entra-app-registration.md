---
title: "Create the Microsoft Entra app registration"
---
# Create the Microsoft Entra app registration

Synchronizing data from Intune, Microsoft Entra ID, Log Analytics, and other cloud data sources is done using application permissions. The steps here configure the permissions required for Power BI to connect to those data sources to get the data.

## Prerequisites

The user performing these steps requires Global Admin and Subscription Admin rights.

## Step 1: Register the application in Microsoft Entra ID

1. Sign in to **portal.azure.com** or **entra.microsoft.com** using a global administrator account.
1. Search for and select **App registrations**.
1. Select **New registration**.
   ![](../../images/New_Registration-1024x491.png)
1. Enter a **Name** for the application. (This will not be seen by anyone other than admins.)
1. Specify who can use the application as **Accounts in this organizational directory only**.
1. Select **Register**.
   ![](../../images/Register_App-788x1024.png)

## Step 2: Add Microsoft Graph permissions

1. On the app registration page select **API Permissions**.
   ![](../../images/API_Permissions-1024x530.png)
1. Remove the **User.Read** permission.
   ![](../../images/Remove_User_Read-1024x277.png)
1. When prompted, select **Yes, remove**.
   ![](../../images/yes_remove-1024x185.png)
1. Select **Add a permission**.
   ![](../../images/add_permission-1024x425.png)
1. Select **Microsoft Graph**.
   ![](../../images/MS_graph-1024x434.png)
1. Select **Application permissions**.
   ![](../../images/application_permissions-1024x403.png)
1. Search for **DeviceManagement** and select these permissions. Do not select **Add permissions** yet — you add several permissions before applying them.
    - **DeviceManagementApps.Read.All**
    - **DeviceManagementConfiguration.Read.All**
    - **DeviceManagementManagedDevices.Read.All**
    - **DeviceManagementRBAC.Read.All**
    - **DeviceManagementServiceConfig.Read.All**

    ![](../../images/Device-Management-Permissions-692x1024.png)
1. Search for **Directory** and select **Directory.Read.All**.
   ![](../../images/Directory-Permissions-1024x715.png)
1. Search for **AuditLog** and select **AuditLog.Read.All**.
   ![](../../images/Audit-Log-Permissions-1024x615.png)
1. Search for **Policy** and select **Policy.Read.All**.
   ![](../../images/Policy-with-CAP-1024x883.png)
1. (Optional — only for Windows 365 / Cloud PC) Search for **CloudPC** and select **CloudPC.Read.All**.
   ![cloudpc readall](../../images/cloudpc_readall-1024x774.png)
1. Search for **Reports**, select **Reports.Read.All**, and select **Add permissions**.
   ![](../../images/Reports-Permissions-plus-add-693x1024.png)

## Step 3: Add Log Analytics permissions

!!! note "Only required for the Custom Inventory solution"
    Skip this step if you do not plan to use the Custom Inventory solution.

1. Select **Add a permission**.
   ![](../../images/Add-Another-Permission-1024x566.png)
1. Select **APIs my organization uses**.
   ![](../../images/API-for-My-Org-1024x626.png)
1. Search for **Log Analytics** and select **Log Analytics API**.
   ![](../../images/Log-Analytics-API-1024x429.png)
1. Select **Application Permissions**.
   ![](../../images/Log-Analytics-Applicattion-Permissions-1024x359.png)
1. Select **Data.Read** and select **Add permissions**.
   ![](../../images/Log-Analytics-Data.Read_-692x1024.png)

## Step 4: Grant admin consent

1. Select **Grant admin consent** for your tenant.
   ![](../../images/Grant-Admin-Consent-1024x667.png)
1. Select **Yes** at the prompt.
   ![](../../images/Admin-Consent-Yes-1024x108.png)

## Step 5: Add a client secret

1. Select **Certificates & secrets**, then select **New client secret**.
   ![](../../images/Certificates-and-Secrets-1024x569.png)
1. Enter a **Description**, select a value for **Expires**, and select **Add**.
   ![](../../images/Add-a-client-secret-479x1024.png)
1. Record the **Value** as the Microsoft Entra ID Client Secret. The value displays only once — if you fail to record it here, you must create a new client secret.
   ![](../../images/Client-Secret-Value-1024x203.png)

## Step 6: Record the application IDs

1. Select **Overview**.
1. Record the **Application (client) ID** as the Microsoft Entra ID Client ID. You use this later in the installation.
1. Record the **Directory (tenant) ID** as the Microsoft Entra ID Tenant ID. You use this later in the installation.
   ![](../../images/Overview-1024x228.png)

The Microsoft Entra app registration is now complete.
