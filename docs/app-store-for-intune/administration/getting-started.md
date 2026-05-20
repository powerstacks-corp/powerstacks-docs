---
title: "Getting started"
description: "First-time admin orientation for the App Store for Intune portal, including dashboard layout and the Setup Wizard."
---

# Getting started

After initial deployment and Entra ID configuration (see [Setup Guide](../installation/setup-guide/)), most portal configuration can be done directly through the Admin Dashboard.

### Accessing the Admin Dashboard

1. Sign in to the portal with an account that is a member of the Admin Group
2. Select **Admin** in the navigation menu
3. The admin portal uses an Intune-style left-rail navigation (v1.28.0+) grouped into four sections that mirror the Microsoft Intune admin center layout. If you've used Intune, the structure should already feel familiar:

   **Apps**
   - **App Management**, manage apps synced from Intune (visibility, approval workflows, deployment options, version rollback)
   - **App Catalog**, browse the public WinGet repository and publish apps to Intune
   - **App Upload** *(v1.29.0+)*, upload custom `.msi` installers for apps that aren't in WinGet
   - **App Updates**, track and deploy update versions for published apps with ring-based rollouts

   **Approvals**
   - **Pending Approvals**, review and approve/reject requests

   **Reports**
   - **Analytics**, request volume, approval throughput, install outcomes, ROI calculator
   - **Store Health**, operational metrics for the portal itself (request volume, deploy pipeline, error rates, latency)
   - **Activity Log**, full timeline of packaging jobs and update deployments

   **Store Administration**
   - **Settings**, authorization, deployment defaults, automation policies, WinGet integration
   - **Branding**, logo, favicon, brand colors, footer
   - **Communications**, company info, notification recipients, Terms of Service, per-event toggles
   - **License**, PowerStacks license activation and entitlement status

### Setup Wizard

For first-time setup or to reconfigure the portal, use the **Setup Wizard**:

1. Go to **Admin** > **Settings** tab
2. Select the **Setup Wizard** button
3. Follow the guided steps:
   - **Welcome** - Overview of setup steps
   - **License** - Enter and validate your PowerStacks license key
   - **Access Groups** - Configure Admin and Approver Entra ID groups
   - **Email Notifications** - Set up email settings for notifications
   - **Sync Apps** - Import apps from your Intune tenant

The wizard saves your settings as you progress through each step. You can skip the wizard at any time and configure settings manually.

!!! note
    The License step is required for the portal to be fully operational. Without a valid license, users will see warning banners and some features may be restricted.

**Quick reference commands** (shown in wizard completion):

| Component | Command |
|-----------|---------|
| API (includes packaging service) | `cd src/AppRequestPortal.API && dotnet run` |
| Web | `cd src/AppRequestPortal.Web && npm start` |
