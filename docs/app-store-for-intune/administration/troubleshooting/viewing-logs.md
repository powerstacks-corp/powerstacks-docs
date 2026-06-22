---
title: "Viewing logs"
description: "Where to find App Store for Intune logs: Application Insights queries, the App Service log stream, packaging job status, and background services."
---

# Viewing logs

The App Store for Intune uses multiple logging destinations. Each serves a different purpose.

### Application Insights (recommended)

**Best for:** Detailed error traces, background service logs, performance monitoring

**Location:** Azure Portal → Your App Service → Application Insights → Logs

**Common queries:**

**1. View recent errors (last 1 hour)**
```kusto
traces
| where severityLevel >= 3  // Warning, Error, Critical
| where timestamp > ago(1h)
| order by timestamp desc
| project timestamp, severityLevel, message, operation_Name
| take 100
```

**2. Packaging service logs**
```kusto
traces
| where message contains "PackagingQueueService"
| order by timestamp desc
| take 100
```

**3. Search for specific package errors**
Replace `Google.GoogleDrive` with your package ID:
```kusto
traces
| where message contains "Google.GoogleDrive"
| order by timestamp desc
| take 50
```

**4. View all logs for a specific job ID**
Replace `abc123` with your job ID:
```kusto
traces
| where message contains "abc123"
| order by timestamp desc
| take 100
```

**5. WinGet cache background service**
```kusto
traces
| where message contains "WingetCacheStreamingService"
| order by timestamp desc
| take 100
```

**6. Failed requests (500 errors)**
```kusto
requests
| where resultCode >= 500
| where timestamp > ago(1h)
| order by timestamp desc
| take 50
```

---

### App Service log stream

**Best for:** Real-time monitoring, startup issues, general web app logs

**Azure CLI:**
```bash
# Enable logging (one-time setup)
az webapp log config \
  --name <your-app-name> \
  --resource-group <your-resource-group> \
  --application-logging filesystem \
  --level verbose

# View live logs
az webapp log tail \
  --name <your-app-name> \
  --resource-group <your-resource-group>
```

**Azure Portal:**
1. Go to your App Service
2. Select **Log stream** from the left menu
3. Choose **Application Logs**

**Note:** Background services (packaging, cache refresh) may not appear in log stream. Use Application Insights for those.

---

### Packaging job status

**Best for:** Quick status check, user-facing error messages

**Location:** Admin Dashboard → Packaging Jobs tab

**What you see:**
- Job ID
- Package ID
- Status (Pending, Downloading, Packaging, Uploading, Completed, Failed)
- Error message (if failed)
- Start/completion time

**Limitations:**
- Error messages may be truncated
- Detailed stack traces not shown
- For full error details, use Application Insights

**Example job statuses:**

| Status | Description |
|--------|-------------|
| Pending | Job queued, waiting to be processed |
| Downloading | Downloading installer from WinGet repository |
| Packaging | Creating .intunewin package |
| Uploading | Uploading package to Intune |
| Completed | Successfully published to Intune |
| Failed | Error occurred (see error message) |

---

### Background service logs

Background services run independently of HTTP requests. Their logs appear in Application Insights, not the live log stream.

**Services that run in the background:**
1. **PackagingQueueService** - Processes WinGet packaging jobs
2. **WingetCacheStreamingService** - Refreshes cached packages daily
3. **RequestEscalationService** - Escalates stale approval requests
4. **AppSyncService** - Syncs apps from Intune
5. **LicenseValidationService** - Validates PowerStacks license

**How to view:**

Use Application Insights with service-specific queries:

```kusto
// Packaging service
traces
| where message contains "PackagingQueueService"
| order by timestamp desc
| take 100

// Cache refresh service
traces
| where message contains "WingetCacheStreamingService"
| order by timestamp desc
| take 100

// Request escalation service
traces
| where message contains "RequestEscalationService"
| order by timestamp desc
| take 100
```

---

### Verifying Application Insights is enabled

Application Insights is critical for monitoring and troubleshooting. Follow these steps to verify it's enabled and working:

**1. Check if Application Insights resource exists**

Azure Portal → Resource Group → Look for resource named like `apprequest-insights-{uniqueId}`

If missing, the ARM template deployment may have failed. Redeploy using the latest template.

**2. Verify connection string is set**

Azure CLI:
```bash
# View all app settings
az webapp config appsettings list \
  --name <your-app-name> \
  --resource-group <your-resource-group> \
  --query "[?name=='APPLICATIONINSIGHTS_CONNECTION_STRING']"
```

Azure Portal:
1. Go to your App Service
2. Settings → Environment variables
3. Look for `APPLICATIONINSIGHTS_CONNECTION_STRING`
4. Value should start with `InstrumentationKey=...`

**If missing:** The ARM template sets this automatically. If deploying manually, copy the connection string from the Application Insights resource.

**3. Verify Application Insights is not disabled**

Azure Portal:
1. Go to your App Service
2. Settings → Application Insights
3. Ensure it shows "Connected" or "Enabled"
4. If it says "Disabled":
   - Select "Turn on Application Insights"
   - Select your existing Application Insights resource
   - Select "Apply"

**4. Test if logs are flowing**

**A. Check startup logs:**
```kusto
traces
| where message contains "Application Insights"
| order by timestamp desc
| take 10
```

You should see a message like:
```
Application Insights is configured with connection string: InstrumentationKey=...
```

**B. Generate test traffic:**
1. Visit your portal homepage
2. Go to a few pages
3. Wait 2-3 minutes for logs to appear

**C. Query for recent activity:**
```kusto
requests
| where timestamp > ago(10m)
| order by timestamp desc
| take 20
```

If you see results, Application Insights is working correctly.

**5. Common issues**

**No logs appearing:**
- **Wait 2-5 minutes** - There's a delay before logs appear
- Check if the connection string is set correctly
- Restart the App Service to reinitialize Application Insights
- Verify the Application Insights resource isn't disabled or deleted

**"Application Insights was disabled" message:**
- This can happen if you manually disabled it in the portal
- Follow step 3 above to re-enable it
- The ARM template configures it automatically on deployment

**Connection string present but no data:**
- Verify the connection string matches the Application Insights resource
- Check if the Application Insights resource has any data (Portal → Application Insights → Logs)
- Restart the App Service

**6. Manual configuration (if needed)**

If Application Insights isn't working after deployment:

```bash
# Get the connection string from Application Insights
az monitor app-insights component show \
  --app <insights-name> \
  --resource-group <resource-group> \
  --query "connectionString" -o tsv

# Set it in App Service
az webapp config appsettings set \
  --name <app-name> \
  --resource-group <resource-group> \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="<connection-string>"

# Restart the app
az webapp restart \
  --name <app-name> \
  --resource-group <resource-group>
```
