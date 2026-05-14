---
title: "User Experience"
description: "How end users browse the app catalog, request apps, track status, and submit new app requests."
---

# User Experience

### Browsing Apps

The portal provides a Microsoft Store-style browsing experience:

**Home Page:**

- Hero section featuring a prominently displayed app
- Featured apps carousel with navigation controls
- Category sections showing apps grouped by category
- Quick links to Browse Apps and My Requests
- Platform badges (Windows, iOS, Android, macOS, Web) on app cards
- "New" badges on apps added within the last 14 days

**Browse Apps Page:**

- Search apps by name, publisher, or description
- Filter apps by category using the dropdown
- Filter apps by platform (Windows, iOS, Android, etc.)
- Featured apps section at the top
- Apps organized by category with platform badges

**Visual Indicators:**

- **Platform badges** - Show the app's target platform with icons (Windows, iOS, Android, macOS, Web)
- **"New" badge** - Green badge on apps added within the last 14 days
- **"Featured" badge** - Gold badge on featured apps
- **Price indicator** - Shows cost or "Free" label

**App Detail Page:**

When users click on any app card, they see a detailed view including:

- Large hero banner with app icon and blurred background
- App name, publisher, and category badges
- "Featured" badge if applicable
- **Get** button to request the app
- Price or "Free" indicator
- Full description
- App information (Publisher, Version, Category, Platform, Approval status)

### How Users Request Apps

Users can request apps in two ways:

**Quick Request (Get button):**

1. Click the **Get** button on any app card (Home, Browse Apps, or App Detail page)
2. The request modal opens directly
3. If Device assignment, select the target device
4. Enter optional justification
5. Click **Submit Request**

**From App Detail Page:**

1. Click on an app card to open the App Detail page
2. Review the app description and information
3. Click the **Get** button
4. Complete the request form and submit

### Request Status Flow

| Status | Description |
|--------|-------------|
| **Pending** | Request is awaiting approval |
| **Approved** | All approvals complete, processing assignment |
| **Rejected** | Request was rejected by an approver |
| **Processing** | System is adding user/device to AAD group |
| **Completed** | User/device successfully added to group |
| **Failed** | Error occurred during processing |

### My Requests

Users can view their request history by clicking **My Requests** in the navigation. This shows all requests they've submitted with current status.

### Request New App

Users can request apps that aren't in the catalog by clicking the **+ Request New App** button on the Browse Apps page.

#### How It Works

1. User fills out the form with app name, publisher, description, and optional download URL
2. The portal sends an email notification to **all members of the Admin Group**
3. The email includes:
   - Requestor name and email
   - App name and publisher
   - Business justification provided by the user
   - Download URL (if provided)
   - Suggestions for how to add the app (Winget catalog or manual upload)
4. The request is logged in the audit trail

#### Admin Actions

When you receive a new app request email:

1. **Evaluate the request**: Is this app appropriate for your organization?
2. **Find the app**:
   - Check the App Catalog in Admin Dashboard for easy publishing
   - Search for the app in Intune if it's already available
   - Download from the vendor if needed
3. **Add to portal**:
   - Use App Catalog to publish directly to Intune, or
   - Manually add the app to Intune and sync
4. **Configure visibility**: Make the app visible in the portal
5. **Notify the user**: Reply to the email or notify the user directly

#### Configuration

The Request New App feature uses your existing email notification settings:

- **Admin Group**: Members receive the notification emails
- **Email Settings**: Uses the same `Mail.Send` configuration as other notifications

No additional configuration is required. If email notifications are disabled, the feature will return an error to the user.
