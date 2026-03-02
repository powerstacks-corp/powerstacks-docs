---
title: "Install Power BI Gateway"
---
# Install The Power BI Gateway
A Microsoft Power BI date gateway an app that you install in on an on-premises device. The on-premises data gateway acts as a bridge to provide quick and secure data transfer between the ConfigMgr SQL database and the Power BI service. There are two data gateway types; personal and standard. Only the standard gateway is supported by BI for SCCM. Most customers install the gateway on the ConfigMgr primary site server or the CAS. .NET Framework 4.8 is required for the gateway. If .NET Framework 4.8 is not already installed a reboot is required to install it. If .NET Framework 4.8 is installed no reboot is required when installing the gateway. The gateway is available from [Microsoft here](https://go.microsoft.com/fwlink/?LinkId=2116849&clcid=0x409). It is very important to keep the gateway app updated, a new version is released each month and there is no way to configure it to auto update. Many customers experience data synchronization failures due to not updating the gateway, for this reason we recommend updating the gateway app at least every 3 months.

**Pre-requisites:**The gateway communicates on the following outbound ports: TCP 443, 5671, 5672, and from 9350 through 9354. The gateway doesn't require inbound ports. For a detailed list of URL's, ports, and IP's that need to be allowed please see this [Microsoft Article](https://docs.microsoft.com/en-us/data-integration/gateway/service-gateway-communication#ports).

### Step 1





1. Download the gateway and start the installation.
1. In the gateway installer, keep the default installation path.
1. Accept the **terms of use**.
1. Select **Install**.
![](images/install-path.png)
### Step 2





1. Enter the same email address that was used to install BI for SCCM.
1. Select **Sign in**.
![](images/email-address.png)
### Step 3





1. Select **Register a new gateway on this computer.**
1. Select **Next**.
![](images/register-gateway.png)
### Step 4





1. Enter a **Name** for the gateway.
1. Enter a memorable **recovery key.** You will only need this key if you ever want to recover or move your gateway
1. Select **Configure**.
![](images/configure-gateway.png)
### Step 5





1. Select **Close**.
![](images/summary-screen.png)
