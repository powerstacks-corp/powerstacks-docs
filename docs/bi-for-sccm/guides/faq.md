---
title: "FAQ"
---
# Frequently Asked Questions

### The Power BI Gateway is not connecting. What should I check?

1. Confirm the gateway is **online** in the Power BI service under **Settings** > **Manage connections and gateways**.
2. Verify the gateway has network access to the ConfigMgr SQL database server.
3. Ensure the Windows service account running the gateway has the required SQL permissions.
4. Check that the SQL Server port (default **1433**) is not blocked by a firewall.

### How do I configure database access for BI for SCCM?

You need to provide the gateway with credentials to access the ConfigMgr database. See [Configure Database Access](configure-database-access.md) for the step-by-step process.

### My inventory extension data is not appearing in the reports. What should I check?

1. Verify the WMI class or hardware inventory extension has been added to the ConfigMgr **Default Client Settings** > **Hardware Inventory** > **Set Classes**.
2. Run a hardware inventory cycle on a test device and confirm the data appears in **Resource Explorer** in the ConfigMgr console.
3. Allow time for the data to flow from ConfigMgr to the SQL database and then to Power BI on the next refresh.

### How often should I refresh my dataset?

We recommend configuring your dataset to refresh at least **once per day**. Power BI allows up to 8 scheduled refreshes per day depending on your license.

### What does the AD User Discovery feature do?

AD User Discovery enriches device records with user information such as department, manager, and office location from Active Directory. See [AD User Discovery](ad-user-discovery.md) for configuration steps.

### How do I fix broken visuals after an upgrade?

When we rename fields in a new version, any visualization containing a renamed field will appear broken (showing an exclamation point on the affected columns). To fix this:

1. Open the page containing the broken visual in **Edit** mode.
1. Select the broken visualization.
1. On the **Visualizations pane**, find the columns with an exclamation point ("!").
1. Select the "**X**" to remove the old column from the visualization.
1. On the **Data pane**, search for the new field name (check the [Release Notes](../release-notes/index.md) for the renamed fields).
1. Add the new field by placing a checkmark next to it.
1. Rearrange the field order if needed by dragging it in the Visualizations pane.
1. **Save** the changes.

!!! tip
    Always review the [Release Notes](../release-notes/index.md) before upgrading and [back up your custom reports](backup-custom-reports.md) first.
