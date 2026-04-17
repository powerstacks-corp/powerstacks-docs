---
title: "Inventory Environment Variables"
---
# Inventory Environment Variables
Several customers write custom data to the Windows environment variables so that they can track things like OS deployment task sequence name for example. The environment variables are not collected as part of hardware inventory by default. If you would like to be able to report on environment variables, you must enable the class in hardware inventory.

For more information on extending Configuration Manager hardware inventory see [Enable or disable existing classes](https://docs.microsoft.com/en-us/mem/configmgr/core/clients/manage/inventory/extend-hardware-inventory#enable-or-disable-existing-classes) in the [How to extend hardware inventory](https://docs.microsoft.com/en-us/mem/configmgr/core/clients/manage/inventory/extend-hardware-inventory) Configuration Manager documentation page.

**Prerequisites:**

Hardware inventory must be enabled.

### Step 1: Open Client Settings Properties





1. In the Configuration Manager console, go to the **Administration** workspace.
1. Select the **Client Settings** node.
1. Select the **client settings** in which you have configured your hardware inventory settings.
1. On the **Home** tab, in the **Properties** group, choose **Properties**.
![](../images/sccm_client_settings-1024x893.png)
### Step 2: Open Hardware Inventory Classes





1. In the **client settings** dialog, choose **Hardware Inventory**.
1. In the **Device Settings** list, select **Set Classes**.
![](../images/sccm_hinv_set_classes-1024x947.png)
### Step 3: Enable Environment Class





1. In the **Hardware Inventory Classes** dialog, use the **Search for inventory classes** field to search for the **Environment**class.
1. Select the **Environment**class.
1. Select **OK.**
![](../images/cm_environment_vars.png)
### Step 4: Confirm Client Settings





1. In the **client settings** dialog, select **OK**.
![](../images/sccm_client_settings_ok-1024x955.png)
