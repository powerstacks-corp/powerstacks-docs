---
title: "Deploy to Azure"
description: "Deploy App Store for Intune to Azure App Service using the Deploy to Azure button or ARM template, plus troubleshooting for Key Vault and migration issues."
---

# Deploy to Azure

For Azure deployment, use the **Deploy to Azure** button in the repository README, or follow the ARM template deployment steps below.

## Troubleshooting

### Authentication issues

- Verify that all Entra ID app registration settings are correct
- Ensure client IDs and tenant IDs match in configuration files
- Check that admin consent has been granted for all required permissions

### API connection issues

- Verify the API URL in the frontend configuration
- Check CORS settings in the API
- Ensure the API is running and accessible

### Database issues

- Verify the connection string is correct
- Ensure the SQL Server is running and accessible
- Check that migrations have been applied

### Graph API permissions

- Ensure admin consent has been granted for all required permissions
- Verify the client secret is valid and not expired
- Check that the managed identity (when deployed to Azure) has appropriate permissions

## Troubleshooting deployment issues

### Key Vault reference failures (red X marks)

After deploying to Azure App Service, you may see red X marks next to Key Vault references in the Configuration settings, indicating the app cannot access secrets. This is usually caused by Azure AD identity propagation delays.

**Symptoms:**

- App Service Configuration shows red X marks next to Key Vault source settings
- `/health` endpoint returns 503 Service Unavailable
- `/health/migrations` returns error: `Keyword not supported: '@microsoft.keyvault'`
- App logs show "ArgumentException" related to connection strings

**Root cause:**

When deploying with Managed Identity and Key Vault for the first time, there's a 5-15 minute propagation delay for the identity to sync across Azure services. During this time, the App Service cannot resolve Key Vault references.

**Solution:**

1. **Wait for propagation (recommended for new deployments):**
   - After deployment completes, wait 10-15 minutes
   - Refresh the Configuration page to check if red X marks turn to green checkmarks
   - Restart the App Service
   - Verify `/health` and `/health/migrations` endpoints return successful responses

2. **Verify Managed Identity is enabled:**
   - Go to App Service > **Identity** > **System assigned**
   - Ensure Status is **On**
   - Note the **Object (principal) ID**

3. **Verify Key Vault access policy:**
   - Go to Key Vault > **Access policies**
   - Verify an access policy exists for your App Service's Managed Identity
   - Required permissions: **Get** and **List** under Secret permissions
   - If missing, click **+ Create** and add the App Service principal

4. **Check Key Vault networking:**
   - Go to Key Vault > **Networking**
   - Ensure either:
     - "Allow public access from all networks" is selected, OR
     - App Service outbound IPs are added to the firewall allowlist

5. **Verify secret names match:**
   - Go to Key Vault > **Secrets**
   - Verify these secrets exist:
     - `AzureAdClientSecret` (or similar name for the client secret)
     - `SqlConnectionString` (or the name referenced in connection strings)
     - `StorageConnectionString` (if using Azure Storage)
   - In App Service > Configuration, click "Show value" on each Key Vault reference
   - The secret name in the URL must **exactly match** the secret name in Key Vault (case-sensitive)

6. **Force refresh:**
   - Go to App Service > **Restart**
   - Wait 2-3 minutes for cold start
   - Check Configuration again for green checkmarks

**Prevention for future deployments:**

- After deploying ARM template, wait 10 minutes before testing the app
- Use `/health/migrations` endpoint to verify database connectivity before troubleshooting further
- Always check Configuration page for green checkmarks on Key Vault references

### Database migration issues

**Symptoms:**

- `/health/migrations` shows `"pendingCount" > 0`
- Portal returns "Error loading settings" or "Error saving license key"
- Database tables are missing

**Solution:**

1. Verify `/health/migrations` endpoint shows pending migrations
2. Restart the App Service (migrations auto-apply on startup)
3. Wait 2 minutes and check `/health/migrations` again
4. If still pending, check Application Insights logs for migration errors
5. Common errors:
   - **SQL firewall:** Add App Service IP to SQL Server firewall rules
   - **Connection timeout:** Increase timeout in connection string
   - **Permission denied:** Ensure SQL user has db_owner role

For more deployment troubleshooting, see [Troubleshooting](../../administration/troubleshooting.md).

## Next step

Continue to [Configure Email Notifications](configure-email-notifications.md) (optional).
