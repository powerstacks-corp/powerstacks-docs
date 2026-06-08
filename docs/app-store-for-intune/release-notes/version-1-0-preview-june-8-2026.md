---
title: "First Public Preview"
render_macros: false
---

# First Public Preview

App Store for Intune is now available as a public preview. It runs entirely inside your own Azure tenant and gives users a self-service way to request applications while administrators stay in control of what gets deployed.

## Highlights

- **Self-service requests.** Users browse a catalog and request the apps they need. An administrator approves, and the app deploys through Intune.
- **A large catalog, plus your own apps.** Search the full WinGet community catalog of more than 12,000 applications, or upload a custom MSI for anything that is not in it.
- **Hands-off packaging.** Requested apps are wrapped with PSADT, converted to the .intunewin format, and deployed to Intune for you.
- **Approvals that fit your process.** Route requests to admin or approver groups, with per-app control over who signs off.
- **Phased rollouts.** Release updates in rings instead of to everyone at once.
- **Teams notifications.** An optional Teams bot keeps requesters and approvers up to date.

## Built for your tenant

- Everything runs in your Azure subscription. Compute, data, and identity stay with you, and nothing is hosted by PowerStacks.
- Deployment uses a single Entra ID app registration and a managed identity for Microsoft Graph access. There is no client secret to paste or store.

This is a preview and we are adding to it regularly. New release notes will appear here as updates ship.
