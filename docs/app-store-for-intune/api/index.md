---
title: "API Reference"
description: "Programmatic access to App Store for Intune for CI/CD app uploads, automated update triggers, and external system integration."
---

# API Reference

App Store for Intune is API-first. The portal you and your users interact with is a React SPA on top of a REST API; that same API is available for your own automation. Add custom apps from a CI/CD pipeline, trigger update checks in response to a CVE feed, pull approval queue state into a monitoring dashboard, or integrate App Store into any other system that speaks HTTP and JWT.

## What's available

| Surface | Endpoints | Common use |
|---|---|---|
| Apps catalog | `/api/Apps`, `/api/Apps/admin`, `/api/Apps/{id}` | List published apps; read app metadata |
| Custom app upload | `/api/admin/app-upload/inspect`, `/api/admin/app-upload/publish` | Upload an in-house MSI from a CI/CD pipeline |
| WinGet integration | `/api/winget/search`, `/api/winget/publish`, `/api/winget/cache/trigger-sync`, `/api/winget/updates/available` | Search the WinGet catalog, publish from it, trigger update detection |
| Update deployments | `/api/admin/update-deployments`, `/api/admin/update-deployments/{id}/pause`, `/api/admin/update-deployments/{id}/cancel`, `/api/admin/update-deployments/{id}/rollback` | Manage update rollouts |
| Approval workflows | `/api/approval-workflows`, `/api/requests` | Read approval state; submit requests programmatically |
| Reports | `/api/reports`, `/api/audit` | Pull deployment + audit data |

The full endpoint catalog is generated from the running API as an OpenAPI spec. When your App Store instance is running, the spec is at `https://<your-app-store-host>/swagger/v1/swagger.json` and an interactive Swagger UI is at `https://<your-app-store-host>/swagger`. Both require authentication; see [Authentication](authentication.md).

## Where reporting lives

App Store's API covers operational integrations: managing apps, triggering deployments, reading approval state. Anything that's a reporting or data export workload (BI dashboards, data warehouse loads, ad-hoc analytics) lives in [BI for Intune](https://docs.powerstacks.com/bi-for-intune/), not App Store. BI for Intune publishes a Power BI semantic model that you can query through Power BI's native XMLA endpoint, the Power BI REST API, dataflows, or direct export. Microsoft already built the reporting API; App Store doesn't duplicate it.

## What's next

- **[Authentication](authentication.md)** — register an Entra app, grant it API access, request a JWT.
- **[PowerShell examples](examples.md)** — copy-paste-runnable scripts for the three most common automation use cases: CI/CD app uploads, CVE-driven update triggering, and deployment status monitoring.
