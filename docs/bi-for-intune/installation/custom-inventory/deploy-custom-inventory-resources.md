---
title: "Deploy Enhanced Inventory Resources"
render_macros: false
---

# Deploy Enhanced Inventory Azure Resources

This step uses a one-click Azure deployment to create all the infrastructure needed for Enhanced Inventory. The ARM template sets up (or reuses) a Log Analytics Workspace, configures custom tables, and creates the Data Collection Endpoint (DCE) and Data Collection Rule (DCR).

## What the deployment creates

- **Log Analytics Workspace** (new or existing)
- **Custom Log Analytics tables:**
    - `PowerStacksDeviceInventory_CL`
    - `PowerStacksAppInventory_CL`
    - `PowerStacksDriverInventory_CL`
- **Data Collection Endpoint (DCE)**
- **Data Collection Rule (DCR)**
- **Automatic RBAC assignment** (if Enterprise App Object ID is provided)

## Step 1: Deploy to Azure

Click the button below to deploy the required Azure resources:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FPowerStacks-BI%2FEnhancedInventoryDeploy%2Fmain%2Finfra%2Fmain.json)

During deployment you will be prompted for:

- **Workspace selection** — create a new Log Analytics workspace or use an existing one
- **Workspace details** — if using an existing workspace, provide the subscription ID, resource group name, and workspace name
- **Enterprise App Object Id** — paste the Object ID from the previous step ([Create Entra Application](create-inventory-app-registration.md))

!!! tip "Using an existing workspace"
    If you also use **Windows Update for Business Reports** or already have a Log Analytics workspace for BI for Intune, you can reuse it. Select **Use an existing workspace** and provide the workspace details. The new custom tables will be created alongside your existing data.

## Step 2: Automatic RBAC assignment

If the Enterprise Application Object ID was provided during deployment, the template automatically assigns the **Monitoring Metrics Publisher** role to the service principal on the Data Collection Rule (DCR). No manual permission steps are required.

If you left the field blank, you must manually assign the role:

1. Navigate to the deployed **Data Collection Rule** in the Azure Portal.
2. Go to **Access control (IAM)** > **Add role assignment**.
3. Select **Monitoring Metrics Publisher**.
4. Assign it to the Enterprise Application you created earlier.

## Step 3: Capture deployment outputs

After deployment completes:

1. Go to the deployment in the Azure Portal (Resource Group > Deployments).
2. Click on the deployment name.
3. Select the **Outputs** tab.
4. Record the following values:

| Output | Description | Used by |
| --- | --- | --- |
| **DceURI** | Data Collection Endpoint ingestion URI | Inventory scripts |
| **DcrImmutableId** | Data Collection Rule immutable identifier | Inventory scripts |

## Next step

[Configure Windows Inventory Script](windows-inventory-collection-script.md) — update the inventory scripts with your credentials and deployment outputs, then deploy via Intune.
