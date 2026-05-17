---
title: "Database Maintenance"
description: "Azure SQL Database automatic maintenance, backups, scaling guidance, and the rare manual operations."
---

# Database Maintenance

The App Store for Intune uses Azure SQL Database Basic tier, which includes built-in automatic maintenance features. **No manual database maintenance is required.**

### Why no manual maintenance is needed

Azure SQL Database handles all maintenance tasks automatically, including:

| Feature | Description |
|---------|-------------|
| **Automatic Index Tuning** | Azure monitors query patterns and automatically creates, drops, or rebuilds indexes to optimize performance |
| **Automatic Plan Correction** | Detects and fixes query plan regression issues automatically |
| **Automatic Backups** | Point-in-Time Restore (PITR) with 7-day retention (Basic tier), up to 35 days on higher tiers |
| **Geo-Redundant Storage** | Backups are stored redundantly across Azure regions for disaster recovery |
| **Automatic Updates** | Database engine patches and security updates applied automatically with no downtime |
| **Automatic Statistics** | Query statistics are automatically updated to ensure optimal query plans |

### What about maintenance scripts?

You may be familiar with on-premises SQL Server maintenance solutions like [Ola Hallengren's Maintenance Solution](https://ola.hallengren.com/) that schedule index rebuilds, integrity checks, and backup jobs. **These are not needed for Azure SQL Database** because:

1. **Index Maintenance**: Azure's automatic tuning handles index optimization. For a Basic tier database under 2GB, index fragmentation has minimal impact on performance.

2. **Integrity Checks (DBCC CHECKDB)**: Azure runs these automatically. You cannot schedule them yourself on Azure SQL Database.

3. **Backup Jobs**: Azure manages all backups automatically. You cannot create your own backup jobs, instead, you use Azure's built-in Point-in-Time Restore feature.

4. **Statistics Updates**: Azure automatically updates statistics as needed. Manual `UPDATE STATISTICS` commands are rarely necessary.

### Backup and recovery

Azure SQL Database provides built-in backup and recovery capabilities:

| Tier | PITR Retention | Backup Storage |
|------|---------------|----------------|
| **Basic** | 7 days | Geo-redundant (GRS) |
| **Standard** | 35 days | Geo-redundant (GRS) |
| **Premium** | 35 days | Geo-redundant (GRS) |

**To restore your database:**

1. Go to **Azure Portal** > **SQL databases** > your database
2. Select **Restore** in the toolbar
3. Select a restore point (any time within retention period)
4. Azure creates a new database with data as of that point in time

> **Note:** Restoring creates a *new* database, it does not overwrite the existing one. You would rename databases after verifying the restore if needed.

### When to consider scaling up

The Basic tier (2GB, 5 DTUs) is suitable for the App Store for Intune's typical workload. Consider scaling up if you observe:

- Consistent high DTU usage (>80%) in Azure metrics
- Slow query response times
- Timeouts during peak usage

To scale up:

1. Go to **Azure Portal** > **SQL databases** > your database
2. Select **Compute + storage**
3. Select a higher tier (Standard, Premium) or increase DTUs
4. Changes take effect within minutes with minimal downtime

### Manual maintenance (if ever needed)

In rare cases where you need to manually optimize, you can:

```sql
-- View index fragmentation (informational only)
SELECT
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 30
ORDER BY ips.avg_fragmentation_in_percent DESC;

-- Rebuild a specific index if needed (usually not necessary)
ALTER INDEX [IX_AppRequests_UserId] ON [AppRequests] REBUILD;
```

However, for the App Store for Intune's typical data volumes (hundreds to thousands of app requests), this manual intervention is almost never necessary.
