---
title: "Perform-in-place Upgrade"
---
# Perform an In-place Upgrade
We strongly advise customers to always backup their custom reports before performing any in-place upgrades. Failure to do so could result in the loss of your custom reports!
Our backup process consists of creating a new workspace by installing a second instance of BI for Intune. There is no need to configure this instance, it's just a place-holder to which our script, documented in our "[Backup Custom Reports](backup-custom-reports.md)" document, copies all of your custom reports in case something goes wrong during the upgrade. In the unlikely even that the upgrade fails it may be necessary to configure the backup workspace and move it to production.
**Prerequisites:** The user executing these steps should be an administrator of the BI for Intune workspace.

### Step 1





1. Login to **Power BI**.
1. Select **Apps**.
1. Select **Get apps**.
![](images/Get-App-1024x211.png)
### Step 2





1. Select **Template apps**.
1. Search for **BI for SCCM**.
1. Select **BI for SCCM**.
![](images/cm-get-app-1024x661.png)
### Step 3





1. Select **Get It Now**.
![](images/cm-get-it-now-1024x666.png)
### Step 4





1. Enter the required information.
1. Accept the **Microsoft agreement**.
1. Select **Continue**.
![](images/cm-agreement-1024x660.png)
### Step 5





1. Select **Update the workspace and the app**.
1. Select **Install**to accept the terms and conditions.
![](images/cm-workspace-upgrade-1024x605.png)
### Step 6





1. Watch for the **update completed** notification in your browser.
1. The data will revert back to the sample data that comes with BI for SCCM. Start a manual refresh to sync your data.
![](images/Update-Complete.png)
