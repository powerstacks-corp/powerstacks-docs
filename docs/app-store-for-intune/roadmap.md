---
title: "Public roadmap"
description: "Planned features, near-term work, and recently shipped capabilities for the App Store for Intune."
---

# App Store for Intune product roadmap

This document outlines the planned features and current development status of the App Store for Intune.

**Last updated:** May 2026

---

## Current status

The App Store for Intune is a self-service application catalog for Microsoft Intune, allowing users to request apps and administrators to manage approvals and deployments.

### Core features (available now)

- **User self-service**
  - Browse app catalog with search and filtering
  - Request apps with justification
  - Track request status
  - View installation instructions

- **Approval workflows**
  - Multi-stage approval workflows
  - Manager and group-based approval
  - Email notifications for approvers
  - Automatic follow-up reminders

- **Admin management**
  - Sync apps from Microsoft Intune
  - Configure app visibility and approval requirements
  - Manage approval workflows per app
  - Portal branding and customization
  - Terms of Service management

- **Integrations**
  - Microsoft Entra ID authentication
  - Microsoft Intune for app deployment
  - WinGet package catalog for new app discovery
  - Email notifications via Microsoft Graph

- **Reporting**
  - ROI calculator (help desk cost savings)
  - Request reports by app, user, and approval activity
  - CSV export for all reports
  - Trend charts showing request patterns over time
  - Install status tracking with deployment metrics

- **WinGet auto-updates**
  - Track apps published from WinGet for available updates
  - Admin dashboard showing apps with available updates
  - Single-action "Apply Update" to update app versions

---

## Planned features

### Near-term (next 1-2 sprints)

| Feature | Description |
|---------|-------------|
| **Audit trail viewer** | Searchable UI for viewing all portal activity |
| **Enhanced approval reports** | Show what was approved (not just who approved) |
| **Duplicate request prevention** | Check if user already has app access, show "You have access" badge |
| **Application Insights dashboard** | Surface key metrics (latency, errors, active users) in Admin panel |

### Medium-term (3-6 months)

| Feature | Description |
|---------|-------------|
| **Approval delegation** | Delegate approvals when out of office |
| **Escalation rules** | Auto-escalate pending approvals after configurable time |
| **Self-service WinGet requests** | Allow users to request apps from WinGet catalog |
| **PSADT integration** | PowerShell App Deployment Toolkit wrapper generation for enterprise deployments |
| ~~**Disaster recovery**~~ | ~~DR documentation, geo-redundancy options, backup/restore procedures~~ (Completed) |
| **Rate limiting** | API rate limiting for security and performance |

### Long-term (6+ months)

| Feature | Description |
|---------|-------------|
| **Microsoft Teams approvals** | Approve/reject directly from Teams Adaptive Cards |
| **Scheduled update checking** | Automatic WinGet update detection (daily, weekly, Patch Tuesday) |
| **Ring deployments** | Staged rollouts for app updates |
| **iOS/Android store apps** | Full support for mobile app deployment |
| **ServiceNow integration** | Bidirectional ticket sync |

---

## Recently completed

### February 2026

- **Azure Key Vault integration**
  - All secrets (Microsoft Entra ID, SQL, Storage) stored in Key Vault
  - Managed Identity access (no plaintext secrets in App Settings)
  - Soft delete enabled for accidental deletion recovery
  - Automatic deployment via ARM template

- **Disaster recovery and geo-redundancy**
  - Geo-redundant storage (GRS) enabled by default
  - Geo-redundant SQL backups for cross-region recovery
  - Full DR documentation with recovery runbooks
  - Tier 3 (High Availability) manual setup guide

- **Unit test infrastructure**
  - xUnit test framework with Moq and FluentAssertions
  - Test data factories for Apps, Users, Requests
  - Mock services for IIntuneService, IAzureADService, INotificationService
  - In-memory database context for isolated testing
  - GitHub Actions CI workflow for automated testing

- **Microsoft Teams notifications**
  - Send notifications to Teams channels via Incoming Webhooks
  - Rich Adaptive Cards with requestor, app details, and action buttons
  - Configurable notifications for new requests, approvals, and rejections
  - Test button to verify webhook configuration
  - Full documentation in Admin Guide

- **User details in reports**
  - Display department and job title from Entra ID in approval reports
  - Show manager information for requestors
  - Enhanced CSV export with user details

- **AppsAndFeaturesEntries from WinGet**
  - Fetch ProductCode and UpgradeCode from WinGet manifests
  - Improved detection rules for Win32 apps
  - Better uninstall detection using registry entries

- **Unsupported app type filtering**
  - Filter out unsupported app types during Intune sync
  - Cleaner app list without Windows MSI LoB, macOS apps, etc.
  - Automatically removes existing unsupported apps

- **Intune-style toggle switches**
  - New pill-shaped toggle buttons with Yes/No labels
  - Consistent styling across the admin interface

- **Performance improvements**
  - Memory caching for Graph API group membership checks (5-minute cache)
  - Faster loading of packaging jobs page
  - Always-visible cancel button for packaging jobs

- **Intune install status tracking**
  - Real-time deployment status (Pending Install, Installing, Installed, Failed)
  - Background polling service checks Intune every 15 minutes
  - Install status tiles on reports dashboard
  - Error message display for failed installations

- **Dashboard analytics and charts**
  - Trend chart showing requests vs completions over time
  - Top requested apps horizontal bar chart
  - Status distribution breakdown
  - Configurable time ranges (7, 14, 30, 90 days)

- **WinGet auto-updates Phase A+B**
  - Apps published from WinGet are tracked for updates
  - "Check for Updates" dashboard in Admin panel
  - Single-action "Apply Update" to update app versions

- **Terms of Service**
  - Click-through TOS with version tracking
  - Admin management for creating and activating TOS versions
  - User acceptance tracking for compliance

- **Follow-up reminder emails**
  - Configurable reminder interval and count
  - Background service for automated reminders

- **CSV export for reports**
  - Export all report views to CSV
  - Failed requests tile added to dashboard

- **Portal access enforcement**
  - Restrict portal access to specific Entra ID group

- **Microsoft-style header UI**
  - User profile dropdown with sign-out
  - Settings gear with dark mode toggle

### January 2026

- WinGet catalog browser and Win32 packaging
- Microsoft Store-style home page with hero app
- Portal branding customization
- Dark mode with user preference
- Basic reports and ROI calculator

---

## Feature requests

To request a new feature:
1. Check if it's already on the roadmap above
2. Open a GitHub issue with the "enhancement" label
3. Describe the use case and expected behavior

PowerStacks reviews and prioritizes feature requests based on customer impact and alignment with our product vision.

---

## Not currently planned

| Feature | Reason |
|---------|--------|
| Multi-tenant support | Portal is designed for single-tenant deployments |
| Container deployment | App Service works well with in-app updates |
| On-premises deployment | Cloud-first design with Azure dependencies |

---

## Documentation

- [Administration guide](administration/) - Complete administration documentation
- [Setup guide](installation/setup-guide/) - Deployment and configuration instructions
- [User guide](user-guides/) - End user documentation
