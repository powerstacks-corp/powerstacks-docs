---
title: "Configure the Dataset"
---
# Configure The Dataset Parameters
The BI for SCCM dataset contains some parameters that must be configured in order to synchronize data from ConfigMgr to Power BI. Other parameters add additional functionality to BI for SCCM. In this article we will only configure the parameters required for basic functionality. Optional parameters are discussed in other articles within our documentation.

### Step 1





1. Select **Workspaces**.
1. Select the **BI for SCCM** workspace.
![](images/access-sccm-workspace.png)
### Step 2





1. Hover over the bi_for_sccm **Semantic model** to reveal a **kebab menu** (three vertical dots).
1. Select the **kebab menu**.
1. Select **Settings**.
![sccm semantic model](images/sccm_semantic_model-926x1024.png)
### Step 3





1. Expand **Parameters**.
1. Enter the **API Key** that you received from us after completing the [**Request a Trail Key**](http://ec2-44-233-150-244.us-west-2.compute.amazonaws.com/wordpress/getting-started/) form.
1. The **Computer Network IP Address Enable** fields accepts **TRUE/FALSE** values. This field controls whether or not IP Addresses from ConfigMgr inventory are sync'd to Power BI or not.
1. Enter the **ConfigMgr database name** in the **DatabaseName** field.
1. Enter the **Server name** of the SQL Server hosting the ConfigMgr database in the **ServerName** field.
1. The **Software Is Used Days(s)**value is the number of days that installed software must have been used within for the reports to show Is Used = True.
1. The **Software Update Not Required Status Enable**field accepts
1. **TRUE/FALSE** values. This field controls whether or not software updates required by no computers are displayed in Power BI. It's strongly recommended to leave this value as **FALSE**.
1. Select **Apply**.
![](images/cm-dataset-parameters-941x1024.png)
### Step 4





1. Expand **Gateway Connection**.
1. Under **Actions**, expand the toggle button to view the data sources.
1. Select the **Add to gateway** link for the **SQL Server** data source.
![](images/expand-gateway-connection-1-1024x712.png)
### Step 5





1. On the **Data Source Settings** page enter the following.
1. For the **Data Source Name**enter**a meaningful name** to identify this data source.
1. For the **Data Source Type**select **SQL Server**.
1. Enter the **SCCM SQL Server name** in the **Server** field.
1. Enter the **SCCM SQL database**name in the **Database**field.
1. Select **Windows** as the **Authentication Method**.
1. Enter **database reader** user account in the **Username field**. If this is an Active Directory user account you must prefix the username with the domain name and a "". **Do Not** **Use** the "@" sign plus domain name.
1. Enter the password for the database reader account in the **Password** field.
1. Select **Add**.
![](images/cm-new-datasource-1024x874.png)
### Step 6





1. Select **Workspaces**.
1. Select the **BI for SCCM** workspace.
![](images/access-sccm-workspace.png)
### Step 7





1. Select **Datasets + dataflows**.
1. Hover over the **bi_for_sccm** dataset to reveal a **kebab menu** (three vertical dots).
1. Select the **kebab menu**.
1. Select **Settings**.
![](images/cm-dataset-settings-955x1024.png)
### Step 8





1. Expand **Gateway Connection**.
1. Under **Actions**, expand the toggle button to view the data sources.
1. Select the **Add to gateway** link for the **SQL Server** data source.
![](images/expand-gateway-connection-1-1024x712.png)
### Step 9





1. Expand **Parameters**.
1. In the **Maps to** drop-down menu in the **SqlServer** source select the S**QL Server data** source that you created in Step 5.
1. Ignore the warning that your data source can't be refreshed.
1. Select **Apply**.
1. Select Edit credentials.
![](images/cm-maps-to-1-1024x722.png)
### Step 10





1. Select **Anonymous**as the **Authentication Method.**
1. Select **Organizational**as the **Privacy level setting for this data source**.
1. Select **Sign in**.
![](images/cm-powerstacks-data-source.png)
### Step 11





1. Expand **Scheduled refresh**.
1. Select **Add another time**.
1. Enter up to eight times of the of the day for the data to refresh. Depending upon the environment, most customers select 1-3 times per day.
1. Grab something cold to drink, you made it through configuring the dataset. The refresh can take anywhere from 5 minutes to 2 hours depending upon your environment. On average, it's about 30 minutes.
![](images/scheduled-refresh-1024x925.png)
### Step 12





1. Select **Workspaces**.
1. Select the **BI for SCCM** workspace.
![](images/access-sccm-workspace.png)
### Step 13





1. Select **Datasets + dataflows**.
1. Hover over the **bi_for_sccm** dataset to reveal the **Refresh now** button.
1. Select the **Refresh now** button.
1. Grab something cold to drink. You've made it through configuring the dataset. The refresh will take anywhere between 5 minutes and 2 hours depending on the environment, however the average is about 30 minutes.
![](images/cm-refresh-now-1024x455.png)
