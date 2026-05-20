---
title: "Reports and analytics"
description: "Built-in dashboards, install status tracking, by-person reports, and the audit trail with CSV export."
---

# Reports and analytics

The Admin Dashboard includes built-in reporting capabilities to help you understand app request patterns and deployment status.

### Accessing reports

1. Go to **Admin** in the navigation menu
2. The dashboard displays summary tiles at the top
3. Use the tabs to navigate between report views:
   - **Summary** - Overview statistics with install status
   - **Trends** - Visual charts showing request patterns over time
   - **By Person** - Detailed request history by user
   - **Install Status** - Deployment status for approved requests

### Summary dashboard

The Summary view shows key metrics as clickable tiles:

| Tile | Description |
|------|-------------|
| **Total Requests** | Total number of app requests in the system |
| **Pending** | Requests awaiting approval |
| **Approved** | Requests that have been approved |
| **Rejected** | Requests that were rejected |
| **Pending Install** | Approved requests waiting for Intune deployment |
| **Installing** | Apps currently being installed on devices |
| **Installed** | Successfully deployed apps |
| **Install Failed** | Apps that failed to install |

The install status tiles (Pending Install, Installing, Installed, Install Failed) are color-coded for quick identification:

- **Pending Install** (blue) - Deployment pending
- **Installing** (orange) - Installation in progress
- **Installed** (green) - Successfully deployed
- **Install Failed** (red) - Deployment failed

### Trends tab

The Trends tab provides visual analytics to help identify patterns and popular applications.

#### Request trends chart

The main trends chart shows:

- **Requested** (blue line) - Number of new requests per day
- **Completed** (green line) - Number of completed requests per day
- Visual area fills under each line for easy comparison

Use the time range dropdown to view:

- Last 7 days
- Last 14 days
- Last 30 days
- Last 90 days

#### Top requested apps

A horizontal bar chart showing the most frequently requested applications, helping you identify:

- Popular apps that might benefit from auto-approval
- Apps that may need better visibility or promotion
- Patterns in user requests

#### Status distribution

A breakdown showing the distribution of request statuses:

- Total count and percentage for each status
- Visual progress bars for comparison
- Separate sections for request status and install status

### Install status tracking

The portal automatically tracks the deployment status of approved requests for Intune apps.

#### How it works

1. **Initial status**: When a request is approved for an Intune-managed app, the install status is set to "Pending Install"
2. **Background polling**: A background service checks Intune for deployment status every 15 minutes
3. **Status updates**: The portal updates the install status based on Intune's reported deployment state
4. **Final status**: Once installed (or failed), the status stops being polled

#### Install status values

| Status | Description |
|--------|-------------|
| **Not Applicable** | App is not tracked for install status (e.g., WinGet apps) |
| **Pending Install** | Request approved, waiting for Intune to begin deployment |
| **Installing** | Intune is actively installing the app on the device |
| **Installed** | App successfully installed and detected on the device |
| **Install Failed** | Installation failed - check the error message for details |
| **Uninstalled** | App was installed but has since been removed |

#### Viewing install status

**Admin Dashboard:**

1. Go to **Admin** > Reports section
2. View install status counts in the summary tiles
3. Select any status tile to filter by that status
4. Use the **Install Status** tab for detailed view

**Install Status tab:**

The dedicated Install Status tab shows:

- Summary counts for each install state
- List of all requests with their current install status
- Last checked timestamp for each request
- Error messages for failed installations

#### Troubleshooting install status

**Status stuck on "Pending Install":**

- Verify the device is online and connected to Intune
- Check that the user/device is correctly added to the target Microsoft Entra ID group
- Review Intune device sync status in the Intune admin center

**Status shows "Install Failed":**

- Check the error message in the Install Status column
- Common issues:
  - Disk space insufficient
  - App dependencies not met
  - User canceled the installation
  - Device compliance issues blocking deployment

**Status not updating:**

- The polling service runs every 15 minutes
- Check API logs for any errors in the InstallStatusPollingService
- Verify the app registration has `DeviceManagementApps.Read.All` permission

### By person report

The **By Person** tab lets you search for a specific user and view all their app requests:

1. Enter a user's name or email in the search box
2. View their complete request history
3. See status, install status, and timestamps for each request
4. Use the **Retry** button on failed requests to re-attempt group membership

### Audit trail

The **Audit Trail** tab provides a full log of all portal activity for compliance and security monitoring.

#### Accessing the audit trail

1. Go to **Admin** > **Reports** section
2. Select the **Audit Trail** button in the report navigation
3. Use filters to narrow down results

#### Available filters

| Filter | Description |
|--------|-------------|
| **Search** | Free-text search across user email, action, entity, and details |
| **Action Type** | Filter by specific action (e.g., Request.Submitted, App.Suggested) |
| **Entity Type** | Filter by entity type (e.g., Request, App, Settings) |
| **Start Date** | Show events from this date onwards |
| **End Date** | Show events up to this date |

#### Audit log information

Each audit entry includes:

| Field | Description |
|-------|-------------|
| **Timestamp** | When the action occurred |
| **User** | Email address of the user who performed the action |
| **Action** | The type of action performed |
| **Entity Type** | The type of object affected |
| **Entity ID** | Identifier of the affected object |
| **Details** | Additional context (varies by action type) |
| **IP Address** | The IP address of the user |

#### Common actions logged

| Action | Description |
|--------|-------------|
| `Request.Submitted` | User submitted an app request |
| `Request.Approved` | Approver approved a request |
| `Request.Rejected` | Approver rejected a request |
| `Request.Completed` | Request was fulfilled (user added to group) |
| `App.Suggested` | User submitted a new app request via Request New App form |
| `Settings.Updated` | Admin changed portal settings |
| `Apps.Synced` | Admin synced apps from Intune |

#### Exporting audit logs

1. Apply any desired filters
2. Select the **Export CSV** button
3. A CSV file downloads with all matching audit entries
4. Use this for compliance reporting or external analysis

#### Audit log retention

Audit logs are stored indefinitely in the SQL database. There is no automatic purge. For organizations with high volume, consider:

- Periodic export to long-term storage
- Database scaling if performance is affected
- Custom retention policies via direct database management
