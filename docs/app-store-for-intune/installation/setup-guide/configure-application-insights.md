---
title: "Configure Application Insights"
description: "Optional. Enable telemetry and the in-portal Application Insights Dashboard by setting the connection string, App ID, and API Key."
---

# Configure Application Insights

Application Insights provides telemetry logging and the in-portal **Application Insights Dashboard** (performance metrics, error tracking, usage analytics, health monitoring). There are two parts to configure.

## Part A: Connection string (telemetry & logging)

The `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable enables telemetry collection (logs, traces, exceptions). If you deployed via the ARM/Bicep template, this is already set automatically.

**To verify or set manually:**

1. Go to [Azure Portal](https://portal.azure.com) > your **Resource Group**
2. Click on the **Application Insights** resource (e.g., `ai-apprequest-prod`)
3. On the **Overview** page, copy the **Connection String** (click the copy icon)
4. Go to your **App Service** > **Configuration** > **Application settings**
5. Add or verify the setting:
   - **Name:** `APPLICATIONINSIGHTS_CONNECTION_STRING`
   - **Value:** The connection string you copied (starts with `InstrumentationKey=...`)
6. Click **Save** and restart the App Service

## Part B: App ID & API Key (metrics dashboard)

The in-portal Application Insights Dashboard tab uses the Application Insights REST API. This requires an **App ID** and **API Key** which are separate from the connection string.

**Without these settings**, the dashboard still works but uses database-only metrics (no direct Application Insights API queries).

**To configure:**

1. Go to [Azure Portal](https://portal.azure.com) > your **Resource Group**
2. Click on the **Application Insights** resource

**Get the App ID:**

3. In the left menu, click **API Access** (under Configure)
4. Copy the **Application ID** (this is the App ID, NOT the Instrumentation Key)

**Create an API Key:**

5. On the same **API Access** page, click **Create API key**
6. Enter a description: `App Store for Intune Metrics Dashboard`
7. Check **Read telemetry** under permissions
8. Click **Generate key**
9. **Copy the key immediately**. It won't be shown again.

**Add to App Service:**

10. Go to your **App Service** > **Configuration** > **Application settings**
11. Add two settings:
    - **Name:** `ApplicationInsights__AppId`, **Value:** The Application ID from step 4
    - **Name:** `ApplicationInsights__ApiKey`, **Value:** The API key from step 9
12. Click **Save** and restart the App Service

> **Note:** Use double underscores (`__`) in the setting names. This is how ASP.NET Core maps environment variables to the `ApplicationInsights:AppId` configuration path.

> **Note:** For local development, add these to `appsettings.json` under an `ApplicationInsights` section:
> ```json
> {
>   "ApplicationInsights": {
>     "AppId": "your-app-id",
>     "ApiKey": "your-api-key"
>   }
> }
> ```

## Verifying Application Insights

After configuration, verify it's working:

1. Navigate to **Admin** > **Application Insights** tab in the portal
2. You should see performance metrics, error counts, and usage data
3. If you see "Application Insights is not configured", check that both `ApplicationInsights__AppId` and `ApplicationInsights__ApiKey` are set correctly

For detailed troubleshooting, see [Troubleshooting](../../administration/troubleshooting.md).

## Next steps

- Read the [Admin Guide](../../administration/) to learn how to configure the portal through the web UI
- Configure Conditional Access policies for enhanced security
- Set up Azure Monitor and Application Insights for monitoring
- Customize the UI to match your organization's branding
