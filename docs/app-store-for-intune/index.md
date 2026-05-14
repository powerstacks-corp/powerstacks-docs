---
title: App Store for Intune
hide:
  - toc
  - navigation
---

<div class="hero-banner">
  <h1>App Store for Intune <span class="hero-accent">Documentation</span></h1>
  <p>Self-service app catalog, approval workflows, and automated packaging for Microsoft Intune. Deployed entirely in your Azure tenant.</p>
</div>

<div class="quick-links">
  <a class="quick-link-card" href="installation/getting-started/install-app-store-for-intune/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></span>
    <span class="card-title">Install Guide</span>
  </a>
  <a class="quick-link-card" href="administration/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>
    <span class="card-title">Admin Guide</span>
  </a>
  <a class="quick-link-card" href="user-guides/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span>
    <span class="card-title">User Guide</span>
  </a>
  <a class="quick-link-card" href="api/">
    <span class="card-icon"><svg viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg></span>
    <span class="card-title">API Reference</span>
  </a>
</div>

## About App Store for Intune

App Store for Intune is a self-service application catalog and deployment portal for Microsoft Intune. Employees browse a branded catalog, request the apps they need, and the portal routes requests through your approval workflow and deploys via Intune. IT stays in control. Users self-serve. The help-desk queue gets shorter.

Everything runs in your own Azure tenant. The web app, the packaging pipeline, the credentials, and the data all live inside your subscription. There is no vendor cloud holding your Graph API permissions and no third-party service to consent to.

Underneath, every package goes through the same flow: a hash-verified WinGet manifest (or your own custom MSI), wrapped with PSADT v4, converted to `.intunewin`, uploaded as a Win32 app, and assigned through your existing Autopatch deployment rings.

## How the docs are organized

- **Install Guide** — required for every customer. Deploy the Azure resources, register the Entra apps, configure admin access, and stand up the portal. Once the Setup Guide is done you have a working catalog.
- **Admin Guide** — portal settings, app catalog management, approval workflows, communications, reports, and operational concerns like database maintenance and disaster recovery.
- **User Guide** — end-user reference for the employees browsing the catalog and submitting requests.
- **API Reference** — programmatic access to App Store for CI/CD app uploads, automated update triggers, and integration with external systems. Authentication walkthrough plus PowerShell examples.

## Have a question? Ask Pax.

**Pax** is our AI-powered documentation assistant. Click the chat icon in the bottom-right corner to ask a question. Pax can help you find the right guide, troubleshoot setup issues, or explain how a feature works.

<div class="ps-cta-banner">
  <h2>Get started with App Store for Intune</h2>
  <p>Start a free trial or request a pricing quote sized to your environment.</p>
  <div class="ps-cta-banner__buttons">
    <a href="https://powerstacks.com/get-started/" class="ps-cta-banner__btn-primary">Start Free Trial</a>
    <a href="https://powerstacks.com/pricing/" class="ps-cta-banner__btn-secondary">Request a Quote</a>
  </div>
</div>
