---
title: "Troubleshooting the install"
description: "Common issues that surface during or after the App Store for Intune deployment, and how to resolve them."
---

# Troubleshooting the install

## Key Vault reference failures (red X marks)

After the deploy completes, the App Service's Configuration blade may show red X marks next to Key Vault references, and `https://<sitename>.azurewebsites.net/health` may return `503 Service Unavailable`. This is an Azure AD identity propagation delay, not a configuration error.

**Symptoms**

- App Service Configuration shows red X marks next to Key Vault-sourced settings.
- `/health` returns `503 Service Unavailable`.
- `/health/migrations` returns an error mentioning `@microsoft.keyvault`.
- App logs show `ArgumentException` related to connection strings.

**Root cause**

When the App Service's system-assigned managed identity is created during deploy, it takes 5 to 15 minutes to propagate across Azure AD. During that window the App Service cannot resolve its Key Vault references.

**Fix**

1. Wait 10 to 15 minutes, then refresh the Configuration page. The red X marks turn green.
2. Restart the App Service.
3. Verify `/health` and `/health/migrations` return success.

If the references remain unresolved after 30 minutes, check:

- **App Service > Identity > System assigned** — Status is **On**.
- **Key Vault > Access policies** — a policy exists for the App Service's managed identity with **Get** and **List** secret permissions.
- **Key Vault > Networking** — either "Allow public access from all networks" is selected, or the App Service outbound IPs are in the firewall allowlist.
- Each Key Vault reference in App Service Configuration shows a URL where the secret name exactly matches a secret in the vault (case-sensitive).

## Database migration issues

If `/health/migrations` shows `"pendingCount"` greater than zero after the wait period, migrations did not auto-apply.

1. Restart the App Service. Migrations run on startup.
2. Wait two minutes and check `/health/migrations` again.
3. If migrations remain pending, check Application Insights logs for migration errors.

Common causes:

- **SQL firewall** — add the App Service outbound IPs to the SQL Server firewall rules.
- **Connection timeout** — Azure SQL takes a few minutes to be ready on first deploy. Restart the App Service again.
- **Permission denied** — the SQL user the template configured should have the `db_owner` role on the database. If it does not, the template may have failed partway through. Redeploy or contact support.

## Sign-in returns 403 from the admin tab

The first-sign-in account is granted temporary admin access so it can complete the Setup Wizard. If you closed the wizard or signed in with a different account before finishing setup, you may see a 403 from admin endpoints.

Sign in as the original deploying admin (or any Entra ID Global Administrator) and complete the Setup Wizard. After **Finish**, the admin group is persisted and any member of that group can sign in with admin access.

## Sign-in redirect mismatch

The browser returns an Entra ID error like "The reply URL specified in the request does not match the reply URLs configured for the application." This means the frontend app registration's redirect URI list does not include the URL you are signing in from.

Add the URL to the frontend app registration per [Add the production redirect URI](add-redirect-uri.md). The URL must include the trailing slash.

## Graph calls return 403 after sign-in

Sign-in succeeds but operations like **Sync from Intune** return errors with "Insufficient privileges" or similar Graph messages. The App Service's managed identity does not have the required Graph application permissions.

Run the snippet from [Grant Microsoft Graph permissions to the App Service](grant-graph-permissions.md). If you already ran it, verify the assignment per the same page's verification section.

## Further help

For deployment issues not covered here, see the [administration Troubleshooting guide](../../administration/troubleshooting.md) or contact [PowerStacks Support](https://www.powerstacks.com/contact).
