---
title: "Custom Domains"
description: "Configure a custom domain and SSL certificate for your App Store for Intune deployment on Azure App Service."
---

# Custom Domain Configuration

This guide explains how to configure a custom domain (e.g., `apps.yourdomain.com`) for your App Store for Intune deployment on Azure App Service.

## Overview

By default, your portal is accessible via an Azure-assigned URL like:
```
https://apprequestportal-xxxx.azurewebsites.net
```

You can configure a custom domain to provide a more professional, branded experience:
```
https://apps.yourdomain.com
```

## Prerequisites

- Azure App Service running your portal (Basic tier or higher for custom domains with SSL)
- Access to your domain's DNS management
- Admin access to your Entra ID App Registration

## Configuration Order

DNS records have to be in place **before** Azure validates the domain (Azure reads the TXT and CNAME you create at registration time). The portal's in-product Settings tab guides admins through these steps in this order, and so does this reference doc:

1. Configure DNS records at your provider
2. Add the custom domain to Azure (one-click button or manual)
3. Update Entra ID redirect URIs
4. Update the portal's Portal URL setting

## Step 1: Configure DNS Records

### For Subdomains (Recommended)

If using a subdomain like `apps.yourdomain.com`:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | `apps` | `your-app.azurewebsites.net` | 3600 |
| TXT | `asuid.apps` | `<Custom Domain Verification ID>` | 3600 |

The **Custom Domain Verification ID** comes from Azure Portal → App Service → **Settings** → **Custom domains** → **+ Add custom domain** (it's shown in the dialog before you commit, even though you'll come back to actually save in Step 2).

### For Apex/Root Domains

If using your root domain (e.g., `yourdomain.com`):

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | `@` | `<App Service IP Address>` | 3600 |
| TXT | `asuid` | `<Custom Domain Verification ID>` | 3600 |

**Note:** Get the App Service IP address from **Settings** → **Custom domains** → **IP address** in Azure Portal.

### DNS Propagation

DNS changes can take anywhere from a few minutes to 48 hours to propagate globally. You can verify propagation using:
- [dnschecker.org](https://dnschecker.org)
- `nslookup apps.yourdomain.com`
- `dig apps.yourdomain.com`

## Step 2: Add Custom Domain + SSL Certificate to Azure

### Option A: One-Click Deployment (Recommended)

The portal ships an ARM template that adds the custom domain hostname binding **and** provisions a free Azure-managed SSL certificate in a single deployment. From the portal: **Admin → Settings → Custom Domain Setup → Configure Custom Domain in Azure**.

The template lives at:

```
https://raw.githubusercontent.com/powerstacks-corp/app-store-for-intune/main/azuredeploy-customdomain.json
```

DNS records (Step 1) must already be propagated, otherwise Azure's domain validation will fail at deployment time.

### Option B: Manual Configuration

Microsoft's official tutorial is the canonical reference: [Tutorial: Map custom domain to App Service (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain?tabs=root%2Cazurecli#configure-a-custom-domain).

Quick summary:

1. Navigate to **Azure Portal** → **App Services** → your App Service
2. Go to **Settings** → **Custom domains**
3. Click **+ Add custom domain**
4. Enter your custom domain (e.g., `apps.yourdomain.com`)
5. Click **Validate**. This succeeds because DNS from Step 1 is in place.
6. Click **Add**
7. Go to **Settings** → **Certificates** → **+ Add certificate** → **App Service Managed Certificate**
8. Select your custom domain → **Create**
9. Return to **Settings** → **Custom domains** → click your domain → **Add binding** → choose the managed certificate with **SNI SSL**

### Other certificate options (manual only)

The one-click template uses an Azure-managed certificate, which has these limitations:

- Available for App Service Basic tier and above only
- No wildcard domains
- No apex/root domains (use Azure Front Door or a third-party cert)

If your scenario requires a different certificate path, replace step 7 above with one of these:

**Azure Key Vault certificate:**

1. Upload or generate a certificate in Azure Key Vault
2. In App Service → **Settings** → **Certificates** → **+ Add certificate**
3. Select **Import from Key Vault**
4. Choose your Key Vault and certificate
5. Bind to your custom domain

**Bring your own certificate:**

1. Obtain a certificate from a Certificate Authority (CA)
2. Export as PFX/PEM with private key
3. In App Service → **Settings** → **Certificates** → **+ Add certificate**
4. Select **Upload certificate**
5. Upload your PFX/PEM file
6. Bind to your custom domain

## Step 3: Update Entra ID Redirect URIs (Frontend SPA App Registration)

Redirect URIs need to be added to the **Frontend SPA** app registration only. The Backend API app is a confidential client that receives tokens from the SPA, so it doesn't use redirect URIs and doesn't need any change here.

1. Navigate to **Microsoft Entra admin center** → **App registrations**
2. Select your **Frontend SPA** app registration (commonly named *App Store for Intune - Frontend* or similar; if unsure, check `src/AppRequestPortal.Web/src/authConfig.ts`. The `clientId` it imports identifies the SPA app.)
3. Go to **Authentication** → **Platform configurations** → **Single-page application**
4. Add the following redirect URIs:

   ```text
   https://apps.yourdomain.com
   https://apps.yourdomain.com/auth/callback
   ```

5. **Important:** Keep the existing Azure URLs during transition so any open tabs and bookmarks keep working:

   ```text
   https://your-app.azurewebsites.net
   https://your-app.azurewebsites.net/auth/callback
   ```

6. Click **Save**

## Step 4: Update Application Configuration

### Update Portal URL Setting

1. Log into your portal as an admin
2. Go to **Admin** → **Settings**
3. On the **Communications** tab, update the **Portal URL** to your custom domain:

   ```text
   https://apps.yourdomain.com
   ```

4. Click **Save Settings**

This controls the base URL used in email notifications and Teams bot notification links.

### Update Frontend Configuration (if needed)

If you're using environment variables for the API URL, update `REACT_APP_API_URL`:

```env
REACT_APP_API_URL=https://apps.yourdomain.com/api
```

## Step 5: Force HTTPS (Recommended)

Ensure all traffic uses HTTPS:

1. In Azure Portal → App Service → **Settings** → **Configuration**
2. Go to **General settings**
3. Set **HTTPS Only** to **On**
4. Click **Save**

## Step 7: Update Teams Bot Configuration (if enabled)

If you have the Teams Bot enabled for proactive notifications, two things need updating:

### Update Azure Bot Messaging Endpoint

1. Navigate to **Azure Portal** → **Azure Bot** resource → **Configuration**
2. Change **Messaging endpoint** from:
   ```
   https://your-app.azurewebsites.net/api/messages
   ```
   to:
   ```
   https://apps.yourdomain.com/api/messages
   ```
3. Click **Apply**

### Update Teams App Manifest

1. Edit `manifest.json` and add your custom domain to `validDomains`:
   ```json
   "validDomains": [
       "apps.yourdomain.com",
       "your-app.azurewebsites.net"
   ]
   ```
2. Optionally update the `developer` URLs (`websiteUrl`, `privacyUrl`, `termsOfUseUrl`) to use the custom domain
3. Re-zip the manifest files (`manifest.json`, `color.png`, `outline.png`)
4. In **Teams Admin Center** → **Teams apps** → **Manage apps**, find the existing App Store for Intune bot, click it, and upload the updated package

> **Note:** Keeping both domains in `validDomains` ensures the bot continues to work during the transition. You can remove the `.azurewebsites.net` entry later once the custom domain is fully verified.

## Verification Checklist

After configuration, verify:

- [ ] DNS resolves correctly (`nslookup apps.yourdomain.com`)
- [ ] HTTPS works without certificate warnings
- [ ] Portal loads at custom domain
- [ ] Login/authentication works
- [ ] All navigation links use the custom domain
- [ ] Email notifications contain correct URLs
- [ ] Teams bot notifications still arrive (if enabled)

## Troubleshooting

### "Domain verification failed"

- Verify TXT record is correctly configured
- Wait for DNS propagation (up to 48 hours)
- Ensure the verification ID matches exactly

### "Certificate error" or "Not secure"

- Verify SSL certificate is bound to the custom domain
- Check certificate hasn't expired
- Ensure certificate covers your domain (exact match or wildcard)

### "Authentication failed" after domain change

- Verify redirect URIs are updated in Entra ID
- Clear browser cookies and cache
- Check both old and new URLs are in redirect URIs during transition

### "Mixed content" warnings

- Ensure all API calls use HTTPS
- Update any hardcoded HTTP URLs in configuration

## Multiple Environments

If you have multiple environments (dev, staging, production), configure separate custom domains:

| Environment | Custom Domain |
|-------------|---------------|
| Production | `apps.yourdomain.com` |
| Staging | `apps-staging.yourdomain.com` |
| Development | `apps-dev.yourdomain.com` |

Each requires its own:
- DNS records
- SSL certificate
- Entra ID redirect URIs
- Portal URL setting

## Related Documentation

- [Azure App Service Custom Domains](https://docs.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-custom-domain)
- [Azure App Service SSL Certificates](https://docs.microsoft.com/en-us/azure/app-service/configure-ssl-certificate)
- [Entra ID Redirect URIs](https://docs.microsoft.com/en-us/azure/active-directory/develop/reply-url)
