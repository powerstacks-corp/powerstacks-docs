---
title: "Inventory BitLocker"
---

# Inventory BitLocker Status

To populate the data required to see the status of BitLocker encryption, add the **Win32_EncryptableVolume** class to hardware inventory and import the PowerStacks BitLocker MOF to extend it with additional encryption properties. Skipping this step will not generate any errors, but the encryption fields under **Computer Disk** (for example, **Is Encrypted**) will be blank.

The default `Win32_EncryptableVolume` class reports only Device ID, Drive Letter, Persistent Volume ID, and Protection Status. Importing the BitLocker MOF adds **Conversion Status**, **Encryption Method**, and **Is Volume Initialized For Protection**, giving a fuller picture of each volume's encryption state.

For background on extending Configuration Manager hardware inventory, see [How to extend hardware inventory](https://learn.microsoft.com/mem/configmgr/core/clients/manage/inventory/extend-hardware-inventory) in the Configuration Manager documentation.

**Prerequisites:**

1. Hardware inventory must be enabled.
1. Permissions to edit the default hardware inventory settings.

### Step 1: Save the BitLocker MOF File

Download [BitLocker.mof](../../files/BitLocker.mof) and save it somewhere on your Configuration Manager **Primary Site Server** (for example, `C:\Temp\BitLocker.mof`). You will import it in a later step.

### Step 2: Open the Default Client Settings

1. In the Configuration Manager console, go to the **Administration** workspace.
1. Select the **Client Settings** node.
1. Select the **Default Client Settings**.
1. On the **Home** tab, in the **Properties** group, choose **Properties**.

![Selecting Default Client Settings in the Configuration Manager console](../../images/sccm_bitlocker_default_client_settings.png)

### Step 3: Open Hardware Inventory Classes

1. In the **Default Settings** dialog, choose **Hardware Inventory**.
1. In the **Device Settings** list, select **Set Classes**.

![Opening the Hardware Inventory Classes dialog](../../images/sccm_hinv_set_classes-1024x947.png)

### Step 4: Enable the Win32_EncryptableVolume Class

1. In the **Hardware Inventory Classes** dialog, use the **Search for inventory classes** field to search for **Win32_EncryptableVolume**.
1. Select the **Win32_EncryptableVolume** class.

At this point the class reports only the basic properties: **Device ID**, **Drive Letter**, **Persistent Volume ID**, and **Protection Status**. Leave the dialog open and continue to the next step to extend it.

![The Win32_EncryptableVolume class with its default properties](../../images/sccm_Win32_EncryptableVolume-1024x890.png)

### Step 5: Import the BitLocker MOF

1. In the **Hardware Inventory Classes** dialog, select **Import**.

    ![Selecting Import in the Hardware Inventory Classes dialog](../../images/sccm_bitlocker_import.png)

1. Browse to the **BitLocker.mof** file you saved in Step 1, then select **Open**.

    ![Selecting the BitLocker.mof file](../../images/sccm_bitlocker_import_select_mof.png)

1. In the **Import Summary** dialog, leave **Import both hardware inventory classes and hardware inventory class settings** selected. The summary confirms the existing **BitLocker (Win32_EncryptableVolume)** class will be replaced by the imported class. Select **Import**.

    ![The Import Summary dialog confirming the class will be replaced](../../images/sccm_bitlocker_import_summary.png)

### Step 6: Confirm the Extended Properties

After the import, the **Win32_EncryptableVolume** class reports the full set of properties, all selected: **Device ID**, **ConversionStatus**, **Drive Letter**, **EncryptionMethod**, **IsVolumeInitializedForProtection**, **Persistent Volume ID**, and **Protection Status**. Confirm they are all selected, then select **OK**.

![The extended Win32_EncryptableVolume properties after import](../../images/sccm_bitlocker_extended_properties.png)

### Step 7: Confirm Client Settings

1. In the **Default Settings** dialog, select **OK**.

![Confirming the client settings](../../images/sccm_client_settings_ok-1024x955.png)
