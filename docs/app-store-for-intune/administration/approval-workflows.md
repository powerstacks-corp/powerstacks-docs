---
title: "Approval Workflows"
description: "Configure flexible approval workflows for app requests, including linear, pooled, conditional, and SLA-tracked workflows."
---

# Approval Workflows

This document describes how to configure flexible approval workflows for app requests.

## Overview

Each app can be configured to either require approval or not. For apps that require approval, you can configure a custom workflow that determines how requests are processed.

### Requires Approval setting

In the Admin Dashboard's **App Management** tab, select an app row to open its detail view. Under **Approval Settings**, you can configure whether approval is required:

- **No**: Requests are auto-approved immediately. The user/device is added to the target Microsoft Entra ID group without any approval steps.
- **Yes**: Requests go through the configured approval workflow before completion.

Use auto-approval for low-risk apps like free productivity tools. Use approval workflows for licensed software, admin tools, or sensitive applications.

### Workflow types

For apps that require approval, the system supports two types of workflows:

- **Linear**: Specific users must approve in a defined sequence
- **Pooled**: Any member of specified Microsoft Entra ID groups can approve at each stage

You can also require manager approval before the workflow stages begin.

## Workflow configuration

### Settings per app

| Setting | Description |
|---------|-------------|
| `requireManagerApproval` | If `true`, the requesting user's manager must approve first before the workflow stages |
| `workflowType` | Either `Linear` or `Pooled` |
| `stages` | Ordered list of approval stages |

### Linear workflow stages

For Linear workflows, each stage specifies a specific person who must approve:

```json
{
  "stageOrder": 1,
  "approverUserId": "user-azure-ad-object-id",
  "approverEmail": "approver@company.com",
  "approverDisplayName": "John Smith"
}
```

The request moves through each stage in order. Each specified person must approve before moving to the next stage.

### Pooled workflow stages

For Pooled workflows, each stage specifies a Microsoft Entra ID security group:

```json
{
  "stageOrder": 1,
  "approverGroupId": "group-azure-ad-object-id",
  "approverGroupName": "IT Approvers"
}
```

Any member of the specified group can approve the request at that stage. Once approved, it moves to the next stage.

## Request flow

### With manager approval required

1. User submits request
2. Request is sent to user's manager (from Microsoft Entra ID)
3. Manager approves/rejects
4. If approved, request proceeds to workflow stage 1
5. Continue through all workflow stages
6. If all stages approve, request is completed

### Without manager approval

1. User submits request
2. Request proceeds directly to workflow stage 1
3. Continue through all workflow stages
4. If all stages approve, request is completed

## API endpoints

### Get workflow for an app

```
GET /api/apps/{appId}/approval-workflow
```

Returns the current workflow configuration for the app, or a default empty configuration if none exists.

### Create/update workflow

```
PUT /api/apps/{appId}/approval-workflow
```

**Request body (Linear example):**

```json
{
  "requireManagerApproval": true,
  "workflowType": "Linear",
  "stages": [
    {
      "stageOrder": 1,
      "approverUserId": "abc-123-user-id",
      "approverEmail": "first.approver@company.com",
      "approverDisplayName": "First Approver"
    },
    {
      "stageOrder": 2,
      "approverUserId": "def-456-user-id",
      "approverEmail": "second.approver@company.com",
      "approverDisplayName": "Second Approver"
    }
  ]
}
```

**Request body (Pooled example):**

```json
{
  "requireManagerApproval": false,
  "workflowType": "Pooled",
  "stages": [
    {
      "stageOrder": 1,
      "approverGroupId": "group-id-1",
      "approverGroupName": "Department Approvers"
    },
    {
      "stageOrder": 2,
      "approverGroupId": "group-id-2",
      "approverGroupName": "IT Security Team"
    }
  ]
}
```

### Delete workflow

```
DELETE /api/apps/{appId}/approval-workflow
```

Removes the workflow configuration. Apps without a workflow will use the default behavior (immediate approval or rejection based on admin settings).

## Setting up workflows

### Prerequisites

1. **For Pooled workflows**: Create Microsoft Entra ID security groups for each approval stage
2. **For Linear workflows**: Know the Microsoft Entra ID Object IDs of the specific approvers
3. Admin access to the App Store for Intune

### Using the UI (recommended)

1. Go to the **Admin Dashboard** > **App Management** tab
2. Find the app you want to configure
3. Set **Requires Approval** to **Yes** (if not already)
4. Select the **Workflow** button to open the Approval Workflow Editor
5. Configure the workflow:
   - Toggle **Require Manager Approval** if needed
   - Choose the **Workflow Type** (Linear or Pooled)
   - Select **Add Stage** to add approval stages
   - For Linear: Search and select specific users
   - For Pooled: Search and select Microsoft Entra ID groups
6. Select **Save**

See the [Administration guide](../administration/) for detailed UI instructions.

### Using the API

You can also configure workflows programmatically using the API endpoints described below.

### Finding Microsoft Entra ID Object IDs

**For users (Linear):**
1. Go to Azure Portal > Microsoft Entra ID > Users
2. Select the user
3. Copy the "Object ID" from the Overview page

**For groups (Pooled):**
1. Go to Azure Portal > Microsoft Entra ID > Groups
2. Select the group
3. Copy the "Object ID" from the Overview page

## Example scenarios

### Scenario 0: No approval required (auto-approve)

For low-risk apps that don't need any oversight:

1. In Admin Dashboard, find the app
2. Set **Requires Approval** to **No**

Requests are immediately approved and the user/device is added to the target group. No workflow configuration needed.

**Best for:** Free productivity tools, browser extensions, utilities

### Scenario 1: IT Software - Manager + IT approval

Apps that require both manager approval and IT department review:

```json
{
  "requireManagerApproval": true,
  "workflowType": "Pooled",
  "stages": [
    {
      "stageOrder": 1,
      "approverGroupId": "it-approvers-group-id",
      "approverGroupName": "IT Software Approvers"
    }
  ]
}
```

### Scenario 2: Sensitive software - multi-level approval

High-security applications requiring department head and security team approval:

```json
{
  "requireManagerApproval": true,
  "workflowType": "Pooled",
  "stages": [
    {
      "stageOrder": 1,
      "approverGroupId": "dept-heads-group-id",
      "approverGroupName": "Department Heads"
    },
    {
      "stageOrder": 2,
      "approverGroupId": "security-team-group-id",
      "approverGroupName": "Security Team"
    }
  ]
}
```

### Scenario 3: VIP approval chain

Specific executives must approve in order:

```json
{
  "requireManagerApproval": false,
  "workflowType": "Linear",
  "stages": [
    {
      "stageOrder": 1,
      "approverUserId": "cto-user-id",
      "approverEmail": "cto@company.com",
      "approverDisplayName": "CTO"
    },
    {
      "stageOrder": 2,
      "approverUserId": "ciso-user-id",
      "approverEmail": "ciso@company.com",
      "approverDisplayName": "CISO"
    }
  ]
}
```

### Scenario 4: Simple manager approval only

Standard software that just needs manager sign-off:

```json
{
  "requireManagerApproval": true,
  "workflowType": "Pooled",
  "stages": []
}
```

## Database schema

The approval workflow system uses these tables:

- **ApprovalWorkflows**: Stores the workflow configuration per app
- **ApprovalStages**: Stores the ordered stages for each workflow
- **RequestApprovals**: Tracks the approval status at each stage for each request

### Running migrations

After updating to this version, run migrations to create the new tables:

```powershell
cd src/AppRequestPortal.API
dotnet ef migrations add AddApprovalWorkflows --project ../AppRequestPortal.Infrastructure --startup-project .
dotnet ef database update --project ../AppRequestPortal.Infrastructure --startup-project .
```

## Notifications

The approval workflow integrates with multiple notification channels to keep approvers and requestors informed.

### Email notifications

Email notifications are sent automatically when:
- A new request is submitted (to approvers)
- A request is approved (to requestor)
- A request is rejected (to requestor)
- A request moves to the next approval stage (to next-stage approvers)

See the [setup guide](../installation/setup-guide/) Step 9 for email configuration.

### Microsoft Teams notifications

Teams channel notifications provide real-time visibility into approval activity. When enabled:
- **New Request Submitted**: Notification with requestor name, app details, and link to review
- **Request Approved**: Notification with approval details
- **Request Rejected**: Notification with rejection reason

Teams notifications are sent to a channel via Incoming Webhook, so all channel members see the activity. Approvers select through to the portal to take action.

See the [Administration guide](../administration/) for Teams setup instructions.

### Actionable email messages (v1.6.1)

Approvers can now approve or reject requests directly from their email without visiting the portal. When enabled, approval emails include Approve/Reject buttons using Microsoft 365 MessageCard format.

**Features:**
- Approve/Reject buttons embedded in email
- Secure token-based authentication
- Works in Outlook, Outlook Web, and other Microsoft 365 email clients
- Idempotency checks prevent double-approval
- Automatic fallback to standard HTML emails if not configured

**Configuration:**
1. Go to **Admin Dashboard** > **Settings** > **Email Notifications**
2. Enable **"Enable actionable email messages"** checkbox
3. Set **"API Base URL for email actions"** (e.g., `https://apprequest.company.com`)
4. Save settings

**How it works:**
1. User submits request
2. Approver receives email with Approve/Reject buttons
3. Approver selects button in email (no sign-in required)
4. Request is immediately approved/rejected
5. Approver sees confirmation message
6. Requestor receives notification of the decision

**Security:**
- Each email contains a unique, single-use action token
- Tokens expire after 7 days or when request is closed
- All email-based actions are logged in audit trail
- Only intended approver can use the token

---

## Advanced workflow features

### Conditional workflows (v1.6.0, UI in v1.8.2)

Configure approval requirements that vary based on app characteristics, requestor department, or other conditions.

> **New in v1.8.2:** Conditional workflows can be configured directly in the Approval Workflow Editor UI. Each approval stage has a "Make this stage conditional" toggle that reveals the condition builder.

**Available conditions:**
- **Department**: Route based on requestor's department (from Microsoft Entra ID)
- **Cost Center**: Route based on requestor's cost center
- **Job Title**: Route based on requestor's job title
- **Location**: Route based on requestor's office location
- **Platform**: Route based on device/app platform (Windows, macOS, iOS, Android, Linux, Web)
- **Request Count**: Route based on number of previous requests
- **Always**: Stage always applies (default)

**Operators:**
- `Equals`, `NotEquals`
- `Contains`
- `GreaterThan`, `LessThan`, `Between`
- `InList`

**Logical combinations:**
- Combine multiple conditions with `AND` or `OR`
- Example: "Department Equals 'Engineering' AND Request Count GreaterThan 5"

**Example: Route by request count**

```json
{
  "workflowConditions": [
    {
      "conditionType": "RequestCount",
      "operator": "GreaterThan",
      "value": "10",
      "resultWorkflowId": "frequent-requester-workflow-id"
    },
    {
      "conditionType": "Department",
      "operator": "InList",
      "value": "Engineering,DevOps,IT",
      "resultWorkflowId": "tech-department-workflow-id"
    }
  ]
}
```

**Use cases:**
- **High-cost apps**: Apps over $500 require finance + IT approval
- **Security tools**: Apps in "Security" category need CISO approval
- **Mobile apps**: iOS/Android apps follow mobile device management approval path
- **Department-specific**: Engineering department gets expedited approval for dev tools

See the [Administration guide](../administration/) for UI configuration instructions.

---

### Per-app acknowledgment requirement (v1.6.1)

Require users to explicitly acknowledge specific terms before requesting certain apps. Useful for:
- Expensive subscriptions ("I understand this is $500/month")
- Compliance requirements ("I agree to complete security training")
- Usage agreements ("I will only use this for business purposes")

**Configuration (per-app):**
1. Go to **Admin Dashboard** > **App Management**
2. Edit the app
3. Enable **"Require acknowledgment before requesting"** checkbox
4. Set **"Acknowledgment Text"** (e.g., "I understand this is a $500/month subscription")
5. Save

**User experience:**
- When requesting the app, users see a required checkbox with your acknowledgment text
- Submit button is disabled until checkbox is checked
- Acknowledgment is recorded in the request audit trail

**Server-side validation:**
- Backend validates that acknowledgment was provided
- Prevents submission without acknowledgment (even if client-side check is bypassed)

---

### SLA tracking (v1.6.0)

Monitor and enforce Service Level Agreements for request processing times.

**SLA status indicators:**
- **On Track**: Request is within SLA target (green)
- **Warning**: Request is approaching SLA breach threshold (yellow)
- **Breached**: Request exceeded SLA target (red)

**Configurable settings:**
1. **SLA Target Hours**: How long requests should be approved (default: 48 hours)
2. **Warning Threshold**: Percentage of SLA at which to show warning (default: 75%)
3. **Business Hours Only**: Whether to count only business hours (M-F, 9am-5pm)

**Email alerts:**
- Sent when requests enter Warning state
- Sent when requests enter Breached state
- Configurable recipient(s)

**Reports:**
- SLA compliance rate (% of requests meeting SLA)
- Average approval time
- Median approval time
- List of at-risk requests
- Breach history

See the [Administration guide](../administration/) for configuration details.

---

### Auto-escalation of stale requests (v1.6.1)

Automatically escalate approval requests that have been pending for too long, ensuring nothing falls through the cracks.

**How it works:**
1. Background service checks every 30 minutes for pending requests
2. Requests older than configured threshold (default: 48 hours) are escalated
3. Email notifications sent to designated escalation contacts
4. Re-escalates every 24 hours if still pending
5. Tracks escalation count on each request

**Configuration:**
1. Go to **Admin Dashboard** > **Settings** > **Request Escalation**
2. Enable **"Enable automatic escalation of stale requests"**
3. Set **"Escalation Threshold (Hours)"** (default: 48)
4. Set **"Escalation Recipient Email(s)"** (comma-separated) OR **"Escalation Group ID"** (Microsoft Entra ID group)
5. Save settings

**Escalation email contents:**
- **Subject**: "⚠️ ESCALATION: Stale App Request - [App Name]"
- **Details**: Requestor, app, days pending, justification, escalation number
- **Action link**: Direct link to review the request in portal

**Use cases:**
- Ensure approvers don't miss urgent requests
- Alert IT managers of bottlenecks
- Provide visibility to executive team
- Meet SLA commitments

**Best practices:**
- Set threshold to 50% of your SLA target (e.g., 24 hours if SLA is 48 hours)
- Use a Microsoft Entra ID group for escalation recipients (easier to manage)
- Monitor escalation frequency, high rates may indicate approval process issues

---

## Troubleshooting

### Approver doesn't receive email
- Verify email notifications are enabled in Admin Settings
- Check spam/junk folder
- Verify approver is in the correct group (for Pooled workflows)
- Check Application Insights logs for email send errors

### Actionable buttons don't work in email
- Verify "API Base URL" is set correctly in Email Notifications settings
- Check that email client supports Microsoft 365 MessageCards (Outlook, OWA)
- Verify action token hasn't expired (7-day limit)
- Check request hasn't already been approved/rejected

### Request stuck in approval
- Check if approver is on vacation (use approval delegation when available)
- Verify manager is set in Microsoft Entra ID (for manager approval workflows)
- Check if request has been escalated (see Request Escalation settings)
- Review audit logs for approval history

### Escalation emails not sending
- Verify Request Escalation is enabled
- Check escalation recipient email/group ID is valid
- Verify background service is running (check Application Insights)
- Confirm threshold has been reached (check request age)

### SLA status incorrect
- Verify SLA settings (target hours, business hours mode)
- Check timezone configuration in Admin Settings
- Review SLA calculation in reports dashboard

---

## See also

- [Administration guide](../administration/) - Detailed UI instructions
- [Setup guide](../installation/setup-guide/) - Initial configuration
- [User guide](../user-guides/) - End-user perspective
