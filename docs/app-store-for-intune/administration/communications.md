---
title: "Communications"
description: "Configure email notifications, Teams bot notifications, approval reminders, escalations, and Terms of Service."
---

# Communications

The Communications tab (formerly "Terms of Service") consolidates all notification, messaging, and company branding settings in one place.

### Company information

Configure your organization's branding details. These fields are used in notification messages and will support further message customization in future releases.

| Setting | Description |
|---------|-------------|
| **Company Name** | Your organization's name, displayed in notifications |
| **Company Logo** | Upload a logo image (PNG/JPEG). Displayed in branded communications |
| **Support Email** | Contact email for support inquiries |
| **Support Phone** | Contact phone number for support |

### Email notifications

Configure how the portal sends email notifications for request submissions and approvals.

| Setting | Description |
|---------|-------------|
| **Enable email notifications** | Toggle to turn email notifications on or off |
| **Send As User ID** | The Microsoft Entra ID Object ID of the user or shared mailbox that will send emails. Find this in Azure Portal > Microsoft Entra ID > Users > [select user] > Object ID |
| **From Address** | The email address displayed in the From field (should match the mailbox) |
| **Portal URL** | The URL of your portal, used in email links to direct users back to the portal |

**Email Events**, when email notifications are enabled, you can toggle individual events:

| Event | Description |
|-------|-------------|
| **Request Submitted** | Notify requestor when their request is submitted |
| **Approval Required** | Notify approvers when their approval is needed |
| **Request Approved** | Notify requestor when their request is approved |
| **Request Rejected** | Notify requestor when their request is rejected |
| **App Installed** | Notify requestor when their app is installed on their device |
| **App Published** | Notify admin when a WinGet app is published to Intune |

> **Note:** The app registration must have the `Mail.Send` Microsoft Graph application permission with admin consent granted.

#### Creating a service account for email notifications

For production deployments, we recommend creating a **dedicated shared mailbox** or service account with minimal permissions rather than using a personal user mailbox. This ensures email delivery is not tied to any individual's account.

**Option A: Shared mailbox (recommended, no license required)**

1. In the **Microsoft 365 Admin Center**, go to **Teams and Groups** > **Shared mailboxes**
2. Select **Add a shared mailbox**:
   - **Name**: `App Store for Intune` (or your preferred name)
   - **Email**: `apprequests@yourdomain.com`
3. Select **Create**
4. Get the Object ID: Go to **Azure Portal** > **Microsoft Entra ID** > **Users** > search for the shared mailbox > copy the **Object ID**
5. In the portal admin settings, set:
   - **Send As User ID**: The Object ID from step 4
   - **From Address**: `apprequests@yourdomain.com`

> Shared mailboxes do not require a Microsoft 365 license and cannot be used for interactive sign-in, making them ideal for automated email sending.

**Option B: Dedicated service account (license required)**

1. In **Azure Portal** > **Microsoft Entra ID** > **Users** > **New user**:
   - **Display name**: `App Store for Intune Service`
   - **User principal name**: `svc-apprequest@yourdomain.com`
2. Assign a **Microsoft 365 license** with Exchange Online
3. **Disable interactive sign-in**: Microsoft Entra ID > Users > [service account] > Properties > **Account enabled** = No (or use Conditional Access to block interactive sign-in)
4. Copy the **Object ID** and configure as with Option A

**Permissions required:**

The portal sends emails using the Microsoft Graph `Mail.Send` application permission via the backend app registration. This permission allows the app to send mail as **any** user in the organization. To limit which mailbox the portal actually uses:

- Configure the **Send As User ID** in the portal settings to the specific shared mailbox or service account Object ID
- Optionally, use an [Exchange Online Application Access Policy](https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access) to restrict the `Mail.Send` permission to only the designated mailbox:

```powershell
# Connect to Exchange Online
Connect-ExchangeOnline

# Create a mail-enabled security group for allowed senders
New-DistributionGroup -Name "App Store Email Senders" -Type Security

# Add the shared mailbox to the group
Add-DistributionGroupMember -Identity "App Store Email Senders" -Member "apprequests@yourdomain.com"

# Restrict the app registration to only send from mailboxes in this group
New-ApplicationAccessPolicy `
    -AppId "<your-api-client-id>" `
    -PolicyScopeGroupId "App Store Email Senders" `
    -AccessRight RestrictAccess `
    -Description "Restrict App Store for Intune to send emails only from the designated mailbox"

# Test the policy (may take up to 30 minutes to propagate)
Test-ApplicationAccessPolicy -AppId "<your-api-client-id>" -Identity "apprequests@yourdomain.com"
```

#### Actionable email messages (Approve/Reject buttons)

When enabled, approval notification emails include **Approve** and **Reject** buttons directly in the email body (Outlook Actionable Messages). Approvers can approve or reject requests without leaving their inbox.

> **Important:** Actionable email buttons require a one-time [provider registration with Microsoft](#registering-with-microsoft-required) and configuring the **Originator / Provider ID** in the portal settings. Without registration, emails are still sent; they contain the standard HTML body with a "Review Request" link to the portal. The Approve/Reject buttons will only appear once registration is complete and the Originator ID is configured.

| Setting | Description |
|---------|-------------|
| **Enable actionable email messages** | Toggle to enable Approve/Reject buttons in approval emails |
| **API Base URL for Email Actions** | The base URL of your API (e.g., `https://apprequest-prod-xxx.azurewebsites.net`). Used for the button callback endpoints. |
| **Originator / Provider ID** | The Provider ID from your Microsoft Actionable Email registration. Required for Outlook to render action buttons. |

**How it works:**

1. When a request requires approval, the email includes an embedded MessageCard with Approve/Reject buttons
2. The MessageCard is embedded in the email `<head>` as `application/ld+json`, Outlook reads this to render action buttons
3. When an approver selects Approve or Reject, Outlook sends an HTTP POST directly to your API
4. The API validates the request using a secure action token and processes the approval
5. **Fallback behavior**: If Outlook doesn't support Actionable Messages, or if the provider is not registered, or if the Originator ID is not configured, the email falls back to the standard HTML body with a "Review Request" link to the portal. Emails are *always sent* regardless of registration status, only the action buttons are affected.

#### Registering with Microsoft (required for action buttons)

Outlook Actionable Messages require a one-time provider registration with Microsoft. Without this registration, Outlook will silently ignore the action buttons and only show the HTML fallback with a "Review Request" link.

1. Go to the [Actionable Email Developer Dashboard](https://aka.ms/actionableemailregistration)
2. Sign in with your Microsoft 365 admin account
3. Select **New Provider** and fill in:
   - **Friendly Name**: App Store for Intune (or your preferred name)
   - **Sender email address**: The From Address configured in your email settings (e.g., `apprequests@company.com`)
   - **Target URL**: Your API Base URL (e.g., `https://apprequest-prod-xxx.azurewebsites.net`)
   - **Scope**: Select **Organization** (your tenant only, auto-approved by tenant admin)
   - **Public Key**: Leave blank (not required for organization-scoped registrations)
4. Submit the registration, organization-scoped registrations are auto-approved by the tenant admin
5. Copy the **Provider ID** (GUID) from your registration
6. In the portal admin settings, paste the Provider ID into the **Originator / Provider ID** field
7. Allow up to 24 hours for the registration to take effect

**Verifying Exchange Online settings:**

If action buttons still don't appear after registration, verify that Actionable Messages are enabled in Exchange Online:

```powershell
# Check organization-level settings (both should be True)
Get-OrganizationConfig | FL ConnectorsActionableMessagesEnabled, SmtpActionableMessagesEnabled

# If disabled, enable them
Set-OrganizationConfig -ConnectorsActionableMessagesEnabled $true -SmtpActionableMessagesEnabled $true

# Check per-mailbox setting (should be True)
Get-Mailbox -Identity apprequests@company.com | FL ConnectorsEnabled
```

> **Important:** Microsoft is transitioning Actionable Messages from External Access Tokens (EAT) to Microsoft Entra ID token authentication. If Microsoft requires Microsoft Entra ID tokens for new registrations, the portal's action endpoints may need to be updated in a future release. See the [Microsoft Entra ID Token documentation](https://learn.microsoft.com/en-us/outlook/actionable-messages/enable-entra-token-for-actionable-messages) for details.

### Microsoft Teams bot notifications

Send personal Teams notifications to approvers and requestors via a Teams Bot. Each user receives individual Adaptive Card messages in their Teams chat. This uses Microsoft Bot Framework proactive messaging.

| Setting | Description |
|---------|-------------|
| **Enable Teams bot notifications** | Toggle to turn Teams bot notifications on or off |
| **Bot App ID** | Your API Client ID (the bot reuses the API app registration) |
| **Test** | Send a test notification to yourself to verify the bot is working |
| **Approval Required** | Notify approvers when their approval is needed |
| **Request Approved** | Notify requestor when their request is approved |
| **Request Rejected** | Notify requestor when their request is rejected |
| **App Installed** | Notify requestor when their app is installed on their device |
| **App Published** | Notify admin when a WinGet app is published to Intune |

#### Prerequisites

1. An **Azure Bot** resource registered in Azure Portal using your API app registration's Client ID (see the [Setup Guide](../installation/setup-guide/))
2. The **Microsoft Teams** channel enabled on the Azure Bot resource
3. The bot **pre-installed for users** via Teams Admin Center setup policies

> No separate `Bot__` environment variables are needed, the bot uses `AzureAd__ClientId`, `AzureAd__ClientSecret`, and `AzureAd__TenantId` directly.

#### Configuring the portal

1. Go to **Admin** > **Communications** tab
2. Scroll to **Microsoft Teams Bot Notifications**
3. Enable **Enable Teams bot notifications**
4. Enter the **Bot App ID** (your API Client ID, the bot reuses the same app registration)
5. Select **Test** to send a test notification to yourself
6. Select which events should trigger notifications
7. Select **Save Settings**

#### How it works

- The bot is pre-installed for users via Teams Admin Center setup policies
- When the bot is installed for a user, Teams sends a `conversationUpdate` event, the portal stores a conversation reference for that user
- To send a notification, the portal retrieves the stored conversation reference and uses Bot Framework proactive messaging
- For **pooled approvals** (group-based), the portal expands the group membership and sends individual messages to each group member
- For **sequential approvals**, only the current stage approvers are notified
- Notifications are sent as **Adaptive Cards** with request details and action buttons

#### Troubleshooting

- **Bot not sending messages**: Verify the bot is installed for the user by checking the `BotConversationReferences` table
- **Test notification fails**: Ensure the bot is installed for your user account first
- **401 errors**: Verify the Azure Bot resource's Microsoft App ID matches your `AzureAd__ClientId` and the client secret is valid
- **Some users don't receive notifications**: The Teams Admin Center setup policy may take up to 24 hours to propagate

> **Note:** No additional Microsoft Graph API permissions are required for Teams bot notifications. Bot Framework handles its own authentication.

### Approval reminders

Automatically send reminder emails for pending approvals.

| Setting | Description |
|---------|-------------|
| **Enable approval reminders** | Toggle to enable/disable automatic reminders |
| **Reminder interval (days)** | Days before the first reminder is sent (default: 2) |
| **Max reminders** | Maximum number of reminders per request (default: 3) |

### Stale request escalation

Automatically escalate requests that have been pending too long.

| Setting | Description |
|---------|-------------|
| **Enable escalation** | Toggle to enable/disable automatic escalation |
| **Escalation threshold (hours)** | Hours before a request is escalated (default: 48) |
| **Recipient email(s)** | Comma-separated email addresses for escalation notifications |
| **Recipient group** | Microsoft Entra ID group whose members receive escalation notifications |

### Terms of Service

The Terms of Service section remains within the Communications tab, allowing admins to create and manage TOS versions that users must accept.
