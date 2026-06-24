---
title: "Multi Admin Approval (MAA)"
description: "How Intune Multi Admin Approval affects App Store app publishing, and how to exclude the App Store so deployments keep working."
---

# Multi Admin Approval (MAA)

Microsoft Intune Multi Admin Approval (MAA) lets an organization require a second administrator to approve sensitive changes before they take effect. As of June 2026, MAA also enforces on application-authenticated Microsoft Graph calls, not only interactive admin actions.

The App Store publishes and assigns apps to Intune through its managed identity, which is an application-authenticated Graph call. If your tenant has an MAA access policy that protects the **Apps** workload, those calls are held for approval and the App Store cannot publish or update apps until you address it.

## Symptoms

Publishing a new app or applying an update from the App Store fails, and the logs show an HTTP 403 response with an `ApprovalRequired` error, or a message that the `x-msft-approval-justification` header is required.

## Check whether this affects you

MAA is opt-in per workload, so this only applies if your tenant has an MAA access policy that covers Apps.

1. In the Microsoft Intune admin center, go to **Tenant administration** > **Multi Admin Approval** > **Access policies**.
2. Look for an active access policy that protects the **Apps** workload. If there is one, the App Store is affected.

## Resolve it: exclude the App Store

To keep the App Store publishing to Intune, exclude its managed identity from MAA enforcement.

1. In the Microsoft Intune admin center, go to **Tenant administration** > **Multi Admin Approval** > **Access policies**.
2. Select the access policy that protects the Apps workload.
3. On the **Exclusions** tab, add the App Store's application. It appears as an enterprise application named after your App Store app service.
4. Save the change. A second administrator must approve the change before the exclusion takes effect.

The exclusion applies only to the App Store's application-authenticated calls. Interactive admin actions in Intune still require MAA approval.

## What the exclusion means

While the App Store is excluded, apps it publishes to Intune are not gated by Intune MAA. If your organization needs approval enforcement on app publishing, native support is planned: see the [product roadmap](../roadmap.md) for Intune MAA integration and an in-app admin publishing approval workflow.

## Related

- [Security overview](security.md)
- [Approval workflows](approval-workflows.md)
