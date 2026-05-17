---
title: "Security Overview"
description: "Security model, Azure resources, permissions, and compliance details for the App Store for Intune."
---

# Security Overview

This document provides full security documentation for the App Store for Intune, including all Azure resources created, permissions granted, and security configurations. It is intended to assist security teams with reviews and compliance requirements.

## Table of contents

1. [Azure resources created](#azure-resources-created)
2. [Identity and access management](#identity-and-access-management)
3. [Microsoft Entra ID app registrations](#microsoft-entra-id-app-registrations)
4. [Managed identity configuration](#managed-identity-configuration)
5. [Network security](#network-security)
6. [Data protection](#data-protection)
7. [Authentication flow](#authentication-flow)
8. [Authorization model](#authorization-model)
9. [Audit logging](#audit-logging)
10. [Security checklist](#security-checklist)
11. [Package verification](#package-verification)

---

## Azure resources created

The ARM template deploys the following resources:

| Resource Type | Name Pattern | Purpose |
|--------------|--------------|---------|
| App Service Plan | `asp-apprequest-{env}` | Hosts the web application |
| App Service | `apprequest-{env}-{unique}` | ASP.NET Core API + React SPA |
| Azure Key Vault | `kv-appreq-{unique}` | Secure secret storage |
| SQL Server | `sql-apprequest-{env}-{unique}` | Database server |
| SQL Database | `AppRequestPortal` | Application data storage |
| Storage Account | `stappreq{unique}` | Queue + blob storage for packaging |
| Application Insights | `ai-apprequest-{env}` | Application monitoring |
| Log Analytics Workspace | `la-apprequest-{env}` | Centralized logging |
| Azure Bot | `bot-apprequest-{env}-{unique}` | Teams proactive messaging (optional) |
| Bot Teams Channel | `{bot}/MsTeamsChannel` | Enables Teams communication (optional) |

### Resource configuration details

#### App Service
- **Runtime**: .NET 8.0 on Linux
- **TLS Version**: Minimum TLS 1.2 enforced
- **HTTPS Only**: Enabled (HTTP redirects to HTTPS)
- **FTPS State**: Disabled (no FTP access)
- **Client Affinity**: Disabled (stateless application)
- **Always On**: Enabled (prevents cold starts)

#### SQL Server
- **TLS Version**: Minimum TLS 1.2
- **Firewall**: Only Azure services allowed (0.0.0.0-0.0.0.0)
- **Authentication**: SQL authentication (username/password)

#### Azure Bot (optional)
- **SKU**: F0 (Free)
- **Location**: Global
- **App Type**: SingleTenant
- **Microsoft App ID**: Reuses the Backend API Microsoft Entra ID App Registration (`AzureAd:ClientId`)
- **Messaging Endpoint**: `https://{app-url}/api/messages`
- **Channels**: Microsoft Teams only
- **Authentication**: Bot Framework handles its own authentication via `ConfigurationBotFrameworkAuthentication` using the same Entra ID client credentials as the API

**Bot Framework Authentication Model:**
- The Azure Bot resource does **not** use a separate App Registration. It shares the Backend API registration.
- Bot Framework validates incoming activities from Teams using the `AzureAd:ClientId`, `AzureAd:ClientSecret`, and `AzureAd:TenantId` configuration values
- Proactive messages are sent via `BotAdapter.ContinueConversationAsync` or `CreateConversationAsync`, authenticated with the same credentials
- No additional Microsoft Graph API permissions are required for Teams bot notifications. Bot Framework handles its own auth channel.

**Data stored:**
- `BotConversationReferences` table stores per-user conversation references for proactive messaging
- Contains: User ID (Microsoft Entra ID object ID), Conversation ID, Service URL, serialized ConversationReference JSON
- Conversation references are encrypted/signed by Bot Framework and tied to the bot credentials that created them
- If bot credentials change, existing conversation references become invalid and must be cleared

---

## Identity and access management

### System-assigned managed identity

The App Service is configured with a **System-Assigned Managed Identity**. This identity is automatically created and managed by Azure.

```json
"identity": {
  "type": "SystemAssigned"
}
```

**Purpose**: The Managed Identity allows the application to authenticate to Azure services without storing credentials in code or configuration.

### Role assignments

The following permissions are granted to the Managed Identity:

| Permission Type | Scope | Purpose |
|----------------|-------|---------|
| Website Contributor Role | App Service | Enables in-app updates via Azure Resource Manager |
| Key Vault Access Policy (Get, List Secrets) | Key Vault | Read application secrets from Key Vault |

**Why Website Contributor?**

The in-app update feature allows administrators to update the application from within the portal. To do this, the application must be able to modify its own `WEBSITE_RUN_FROM_PACKAGE` app setting. The Website Contributor role grants this permission.

**Why Key Vault Access?**

All sensitive secrets (Microsoft Entra ID client secret, SQL connection string, storage connection string) are stored in Azure Key Vault. The Managed Identity needs read access to retrieve these secrets at runtime.

**Scope limitation**: All permissions are scoped to the minimum required resources (not the resource group or subscription), following the principle of least privilege.

```json
{
  "type": "Microsoft.Authorization/roleAssignments",
  "scope": "[concat('Microsoft.Web/sites/', variables('appName'))]",
  "properties": {
    "roleDefinitionId": "[subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'de139f84-1756-47ae-9be6-808fbbe84772')]",
    "principalId": "[reference(resourceId('Microsoft.Web/sites', variables('appName')), '2022-09-01', 'full').identity.principalId]",
    "principalType": "ServicePrincipal"
  }
}
```

---

## Microsoft Entra ID app registrations

Two Microsoft Entra ID App Registrations are required:

### 1. Backend API application (confidential client)

**Application type**: Web application / API

**Authentication**:
- Client ID (stored in App Settings)
- Client Secret (stored in App Settings)

**API permissions (application permissions)**:

| API | Permission | Type | Purpose |
|-----|-----------|------|---------|
| Microsoft Graph | `DeviceManagementApps.Read.All` | Application | Read Intune apps |
| Microsoft Graph | `DeviceManagementApps.ReadWrite.All` | Application | Create/update Intune apps |
| Microsoft Graph | `DeviceManagementConfiguration.Read.All` | Application | Read Intune assignment filters (used by ring deployment settings, required for the filter picker) |
| Microsoft Graph | `DeviceManagementManagedDevices.Read.All` | Application | Count managed devices for licensing |
| Microsoft Graph | `Group.ReadWrite.All` | Application | Create and manage Microsoft Entra ID groups |
| Microsoft Graph | `User.Read.All` | Application | Read user profiles, managers, and group memberships |
| Microsoft Graph | `Directory.Read.All` | Application | Read directory data |
| Microsoft Graph | `Mail.Send` | Application | Send email notifications (optional) |

**Teams bot note**: No additional Microsoft Graph permissions are required for Teams bot notifications. Bot Framework handles its own authentication channel separately from Graph. Do *not* add `TeamsActivity.Send` or similar permissions; they are not used by this application.

**Admin consent**: Required for all application permissions.

**Token configuration**:
- Access tokens issued for: `api://{client-id}`
- Scopes exposed: `access_as_user`

### 2. Frontend SPA application (public client)

**Application type**: Single-page application (SPA)

**Authentication**:
- Client ID only (no secret - public client)
- MSAL.js with PKCE flow

**API permissions (delegated permissions)**:

| API | Permission | Type | Purpose |
|-----|-----------|------|---------|
| Microsoft Graph | `User.Read` | Delegated | Read signed-in user's profile and photo |
| Backend API | `access_as_user` | Delegated | Call backend API on behalf of user |

**Redirect URIs**:
- `https://{app-name}.azurewebsites.net/`
- `https://{custom-domain}/` (if custom domain configured)

---

## Managed identity configuration

### How the managed identity works

1. **Creation**: When the ARM template deploys, Azure automatically creates a service principal in Microsoft Entra ID for the App Service.

2. **Environment variables**: Azure injects these environment variables into the application:
   - `MSI_ENDPOINT` or `IDENTITY_ENDPOINT`: Token endpoint URL
   - `IDENTITY_HEADER`: Secret header for authentication
   - `WEBSITE_SITE_NAME`: App Service name
   - `WEBSITE_RESOURCE_GROUP`: Resource group name
   - `WEBSITE_OWNER_NAME`: Subscription ID

3. **Token acquisition**: The application uses `DefaultAzureCredential` from Azure.Identity SDK to acquire tokens:
   ```csharp
   var credential = new DefaultAzureCredential();
   var armClient = new ArmClient(credential);
   ```

4. **Authorization**: The Managed Identity authenticates to Azure Resource Manager and is authorized via the Website Contributor role assignment.

### What the managed identity can do

- Read and update the App Service's own configuration settings
- Read the App Service's properties
- Restart the App Service
- Read secrets from the provisioned Key Vault (Get, List permissions only)

### What the managed identity can't do

- Access other resources in the subscription
- Modify other App Services
- Write, delete, or manage secrets in Key Vault
- Access SQL Database directly (uses SQL authentication via connection string from Key Vault)
- Deploy or delete resources

---

## Network security

### Inbound traffic

| Protocol | Port | Source | Destination | Purpose |
|----------|------|--------|-------------|---------|
| HTTPS | 443 | Internet | App Service | User access |
| HTTPS | 443 | App Service | Azure SQL | Database connections |
| HTTPS | 443 | App Service | Microsoft Graph | API calls |
| HTTPS | 443 | Bot Framework Service | App Service | Teams bot messages (`/api/messages`) |
| HTTPS | 443 | App Service | Bot Framework Service | Proactive bot notifications |

### App Service network configuration

- **Public Access**: Enabled (internet-accessible)
- **TLS 1.2**: Minimum version enforced
- **HTTPS Only**: HTTP requests redirected to HTTPS
- **IP Restrictions**: None by default (can be configured)

### SQL Server firewall

The SQL Server is configured with the following security controls:

- **Azure Services**: Allowed (firewall rule `AllowAllWindowsAzureIps`)
  - This allows the App Service to connect to the database
  - Other Azure services in the subscription cannot access unless explicitly allowed
- **Public IP Access**: Denied by default
  - No client IP addresses are on the allowlist
  - Database is not accessible from the internet
- **Private Endpoint**: Not configured by default (can be added for enhanced security)

!!! important
    The database is not accessible from the public internet. Only Azure services (such as the App Service) can connect.

To verify SQL firewall rules:
```bash
az sql server firewall-rule list --server <server-name> --resource-group <rg-name>
```

To add a client IP for temporary admin access:
```bash
az sql server firewall-rule create --server <server-name> --resource-group <rg-name> \
  --name "AdminAccess" --start-ip-address <your-ip> --end-ip-address <your-ip>
```

**Remember to remove temporary rules after use.**

### Recommendations for enhanced security

#### Conditional Access policies

We strongly recommend configuring the following Microsoft Entra ID Conditional Access policies for the App Store for Intune. Target these policies at the **Backend API** and **Frontend SPA** app registrations.

| Policy | Description | Why It Matters |
|--------|-------------|----------------|
| **Require MFA** | Require multifactor authentication for all users accessing the portal | Prevents unauthorized access from compromised credentials |
| **Require compliant device** | Only allow access from Intune-compliant devices | Since this portal manages Intune apps, ensuring the requesting device meets compliance is a natural fit |
| **Require managed device** | Only allow access from Microsoft Entra ID joined or hybrid joined devices | Prevents access from personal/unmanaged devices |
| **Block risky sign-ins** | Block sign-ins flagged as medium or high risk by Microsoft Entra ID Identity Protection | Automatically blocks access when suspicious activity is detected (requires Microsoft Entra ID P2) |
| **Restrict by location** | Only allow access from trusted named locations (office IPs, VPN ranges) | Limits exposure to known network boundaries |
| **Sign-in frequency** | Require re-authentication every 8-12 hours | Limits the window of exposure from a stolen session token |

!!! tip "Recommended minimum"
    At a minimum, enable **Require MFA** and **Require compliant device**. These two policies provide strong protection without significant user friction, especially for organizations already using Intune for device management.

!!! note "Admin vs User policies"
    Consider creating a stricter policy for the **Admin Group** (e.g., require phishing-resistant MFA, restrict to trusted locations) since admins can modify portal settings, manage apps, and approve requests.

#### Network security enhancements

1. **Virtual network integration**: Deploy App Service into a VNet
2. **Private endpoints**: Use private endpoints for SQL and storage
3. **IP restrictions**: Limit access to known IP ranges
4. **Azure Front Door**: Add WAF protection

---

## Data protection

### Data at rest

| Data Type | Storage Location | Encryption |
|-----------|-----------------|------------|
| Application data | Azure SQL Database | TDE (Transparent Data Encryption) |
| User settings | Azure SQL Database | TDE |
| Branding assets | Azure SQL Database | TDE |
| Bot conversation references | Azure SQL Database | TDE |
| Logs | Log Analytics | Azure-managed encryption |

### Data in transit

- All communication uses TLS 1.2+
- HTTPS enforced at App Service level
- SQL connections use encrypted connections

### Sensitive data handling

| Data | Storage Method | Notes |
|------|---------------|-------|
| Microsoft Entra ID Client Secret | Azure Key Vault | Referenced via Key Vault reference in App Settings |
| SQL Connection String | Azure Key Vault | Referenced via Key Vault reference in App Settings |
| Storage Connection String | Azure Key Vault | Referenced via Key Vault reference in App Settings |
| User tokens | Session storage (browser) | Not persisted server-side |
| Action tokens | SQL Database | GUID per request, used for email approve/reject |
| Bot conversation references | SQL Database | Conversation IDs and service URLs for Teams proactive messaging |
| Audit logs | SQL Database | Retained indefinitely |

### Secrets management

All sensitive secrets are stored in Azure Key Vault and accessed via Key Vault references:

```
AzureAd__ClientSecret = @Microsoft.KeyVault(SecretUri=https://{vault}.vault.azure.net/secrets/AzureAdClientSecret/)
ConnectionStrings__DefaultConnection = @Microsoft.KeyVault(SecretUri=https://{vault}.vault.azure.net/secrets/SqlConnectionString/)
AzureStorage__ConnectionString = @Microsoft.KeyVault(SecretUri=https://{vault}.vault.azure.net/secrets/StorageConnectionString/)
```

**Key Vault security features:**
- Secrets encrypted at rest with Azure-managed keys
- Soft delete enabled (7-day retention for accidental deletion recovery)
- Access restricted to the App Service's Managed Identity only
- No direct secret access for users or administrators (must use Azure Portal/CLI with appropriate permissions)
- All secret access is logged in Key Vault diagnostic logs

### Secret and key rotation

**Microsoft Entra ID client secret rotation:**

The Microsoft Entra ID client secret has an expiration date (typically 1-2 years). To rotate:

1. **Create new secret** in Azure Portal → Microsoft Entra ID → App Registrations → Your API App → Certificates & secrets
2. **Update Key Vault secret**:
   ```bash
   az keyvault secret set --vault-name <vault-name> --name AzureAdClientSecret --value "<new-secret>"
   ```
3. **Restart App Service** to pick up the new secret:
   ```bash
   az webapp restart --name <app-name> --resource-group <rg-name>
   ```
4. **Delete old secret** from Microsoft Entra ID after confirming the app works

**SQL password rotation:**

1. **Reset password** in Azure Portal → SQL Server → Reset admin password
2. **Update connection string** in Key Vault:
   ```bash
   az keyvault secret set --vault-name <vault-name> --name SqlConnectionString --value "Server=tcp:..."
   ```
3. **Restart App Service**

**Emergency key rotation:**

If you suspect a secret has been compromised:
1. Immediately rotate the affected secret using the steps above
2. Review Key Vault access logs for unauthorized access
3. Review App Service logs for unusual activity
4. Consider rotating all secrets if compromise scope is unknown

### Certificate management

**SSL certificates:**

| Certificate Type | Management | Renewal |
|-----------------|------------|---------|
| Azure-managed (default) | Automatic | Auto-renewed by Azure |
| Custom domain with Azure certificate | Automatic | Auto-renewed by Azure |
| Custom uploaded certificate | Manual | Upload new certificate before expiration |

**Microsoft Entra ID app certificates (optional):**

If using certificate authentication instead of client secrets:
- Monitor expiration dates in Microsoft Entra ID → App Registrations → Certificates & secrets
- Upload new certificate before expiration
- Update Key Vault with new certificate thumbprint

**Monitoring expiration:**

Set up Azure Monitor alerts for:
- Key Vault secret expiration (90 days before)
- Microsoft Entra ID client secret expiration
- SSL certificate expiration (if custom)

```bash
# Check Key Vault secret expiration dates
az keyvault secret list --vault-name <vault-name> --query "[].{name:name, expires:attributes.expires}"
```

---

## Authentication flow

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Browser    │         │   Entra ID   │         │  App Service │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       │  1. Navigate to app    │                        │
       │───────────────────────────────────────────────>│
       │                        │                        │
       │  2. Redirect to sign-in│                        │
       │<───────────────────────────────────────────────│
       │                        │                        │
       │  3. User authenticates │                        │
       │───────────────────────>│                        │
       │                        │                        │
       │  4. Return tokens      │                        │
       │<───────────────────────│                        │
       │                        │                        │
       │  5. API call with token                         │
       │───────────────────────────────────────────────>│
       │                        │                        │
       │                        │  6. Validate token     │
       │                        │<───────────────────────│
       │                        │                        │
       │                        │  7. Token valid        │
       │                        │───────────────────────>│
       │                        │                        │
       │  8. API response       │                        │
       │<───────────────────────────────────────────────│
```

### Token validation

The API validates JWT tokens from Microsoft Entra ID:

1. **Issuer**: Must match Microsoft Entra ID tenant
2. **Audience**: Must match API Client ID
3. **Signature**: Validated using Microsoft Entra ID public keys
4. **Expiration**: Token must not be expired
5. **Claims**: User identity extracted from token

---

## Authorization model

### Role-based access control

| Role | How Assigned | Capabilities |
|------|--------------|--------------|
| User | Any authenticated user | Browse apps, submit requests, view own requests |
| Approver | Member of Approver Microsoft Entra ID Group | Approve/reject requests, view pending approvals |
| Admin | Member of Admin Microsoft Entra ID Group | Full access, manage apps, settings, users |

### Group-based authorization

Authorization groups are configured in the database (`PortalSettings` table):

```sql
AdminGroupId      -- Microsoft Entra ID Group Object ID for admins
ApproverGroupId   -- Microsoft Entra ID Group Object ID for approvers
UserAccessGroupId -- (Optional) Restrict access to specific group
```

### Authorization check flow

```csharp
// Check if user is admin
var userId = User.FindFirstValue("oid");
var isAdmin = await _azureADService.IsUserInGroupAsync(userId, adminGroupId);
```

---

## Audit logging

### What is logged

| Event | Data Captured |
|-------|--------------|
| App request submitted | User ID, App ID, Device ID, Timestamp |
| Request approved/rejected | Reviewer ID, Decision, Comments, Timestamp |
| Settings changed | User ID, Setting changed, Old/New values |
| App sync | User ID, Apps added/updated, Timestamp |
| User sign-in | User ID, IP address, Timestamp |

### Audit log storage

- **Location**: SQL Database (`AuditLogs` table)
- **Retention**: Indefinite (no automatic purge)
- **Access**: Admin-only via Reports section

### Log schema

```sql
CREATE TABLE AuditLogs (
    Id NVARCHAR(450) PRIMARY KEY,
    UserId NVARCHAR(450) NOT NULL,
    UserEmail NVARCHAR(255) NOT NULL,
    Action NVARCHAR(100) NOT NULL,
    EntityType NVARCHAR(100) NOT NULL,
    EntityId NVARCHAR(450) NOT NULL,
    Details NVARCHAR(MAX),  -- JSON payload
    Timestamp DATETIME2 NOT NULL,
    IpAddress NVARCHAR(50) NOT NULL
);
```

---

## Security checklist

### Pre-deployment

- [ ] Microsoft Entra ID App Registrations created with minimum required permissions
- [ ] Admin consent granted for application permissions
- [ ] Strong SQL administrator password configured
- [ ] Admin Group ID configured (**required**, admin access is denied without it)
- [ ] Approver Group ID configured (restricts approver access)

### Post-deployment

- [ ] Verify HTTPS-only access working
- [ ] Test authentication flow
- [ ] Verify role-based access (admin vs. user)
- [ ] Review Microsoft Entra ID sign-in logs
- [ ] Enable Azure Security Center recommendations
- [ ] If Teams bot enabled: verify Azure Bot App ID matches `AzureAd:ClientId`
- [ ] If Teams bot enabled: test bot notification delivery

### Ongoing operations

- [ ] Rotate Microsoft Entra ID client secret annually
- [ ] Review audit logs regularly
- [ ] Monitor failed authentication attempts
- [ ] Update application when security patches released
- [ ] Review and remove unused app permissions

### Optional enhancements

- [ ] Enable Microsoft Entra ID Conditional Access policies (see [Recommended Policies](#conditional-access-policies))
- [ ] Configure Microsoft Entra ID Identity Protection (required for risk-based CA policies)
- [ ] Implement Private Endpoints for SQL and Key Vault
- [ ] Add Azure Front Door with WAF
- [ ] Enable Azure Defender for App Service
- [x] Azure Key Vault for secrets (enabled by default)

---

## Package verification

Apps deployed to Intune via the App Store originate as YAML manifests in the [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs) community repository. Each manifest declares an installer URL and the SHA256 hash that installer must match. The packaging pipeline verifies the downloaded installer against that hash before wrapping it for Intune (`PackagingQueueService.DownloadFromGitHubAsync`).

That hash check defends against a tampered installer at the publisher's download server, but it trusts the manifest itself. The manifest is fetched from `raw.githubusercontent.com` over HTTPS, and anyone able to MITM that connection (or substitute a manifest in a compromised mirror) could feed the pipeline a manifest that points at a malicious installer with a matching hash.

### Verified chain via `source2.msix`

To close that gap, the App Store can verify each package against Microsoft's signed community index. The WinGet client itself uses this same chain (see [`PackagesTable.h` in winget-cli](https://github.com/microsoft/winget-cli/blob/master/src/AppInstallerRepositoryCore/Microsoft/Schema/2_0/PackagesTable.h) for the upstream schema).

**How it works (when `VerifyManifestIntegrity` is enabled):**

1. The portal downloads `source2.msix` from `https://cdn.winget.microsoft.com/cache/source2.msix`.
2. The .msix contains a SQLite database (`Public/index.db`) with a `packages` table: one row per package Microsoft has reviewed and merged into the community repository, with the SHA256 of the package's version data manifest in the `hash` column.
3. Before packaging any WinGet-sourced app, the portal looks the package up in this index. If the package is not present, the packaging job fails with an explicit *"Manifest integrity check failed"* error rather than silently falling back to an unverified path.
4. The downloaded MSIX and extracted SQLite are cached on disk for 12 hours so repeat lookups don't re-download the ~10 MB archive.

**What this protects against:**

- Tampered manifest substituted on the GitHub fetch path. A malicious manifest for a non-existent or non-merged package ID will fail the index lookup.
- An attacker pointing an existing package ID at a different installer. Once paired with the version-data-manifest hash check (planned, see roadmap below), the manifest contents can be cryptographically tied back to what Microsoft moderators reviewed.

**What this does not yet protect against (v1 limitations):**

- The full design (documented internally as the WinGet manifest verification specification) calls for fetching the version data manifest from the Azure CDN by content-addressed URL and verifying its hash against the SQLite value, then doing the same for each per-version merged manifest. v1 implements only the index lookup gate; the hash-of-manifest comparison is a planned v2 enhancement.
- MSIX signature validation against Microsoft's certificate chain (Authenticode-on-MSIX via WinTrust). v1 relies on HTTPS + DNS to `cdn.winget.microsoft.com` as the trust root. A compromised CDN is out of scope for v1; v2 will add full signature validation.

**Configuration:** Admin → Settings → "Verify manifest integrity against Microsoft's signed index". Default is **off** in this release while we soak the feature; once validated in production it will flip to default-on. Admins running internal hardened mirrors of the WinGet repo can leave it off and rely on their mirror's own integrity controls.

**Failure mode:** Verification failures are loud, not silent. The packaging job is marked failed and the error message names the package and explains the integrity check failed. There is no fallback to the unverified path while verification is enabled. The only escape valve is to disable the setting from the Settings page.

---

## Compliance considerations

### Data residency

- All data stored in the Azure region selected during deployment
- No cross-region data replication by default

### Data retention

- Audit logs: Retained indefinitely
- Application data: Retained until manually deleted
- App Insights logs: 90 days default (configurable)

### GDPR considerations

- User data limited to: Name, Email, User ID (from Microsoft Entra ID)
- No sensitive personal data stored
- Data can be exported/deleted upon request via database access

---

## Incident response

### Security event indicators

Monitor for these events in Microsoft Entra ID and App Insights:

1. **Multiple failed sign-ins** from same IP
2. **Unusual geographic access** patterns
3. **Bulk data access** (many API calls in short time)
4. **Privilege escalation** attempts
5. **Configuration changes** outside business hours

### Response actions

1. **Disable App Service** if compromise suspected
2. **Rotate secrets** (Microsoft Entra ID client secret, SQL password)
3. **Review audit logs** for unauthorized access
4. **Revoke user access** if account compromised
5. **Contact Azure Support** for assistance

---

## Contact

For security questions or to report vulnerabilities:
- Email: info@powerstacks.com
