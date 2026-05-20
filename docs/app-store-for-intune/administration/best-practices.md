---
title: "Best practices"
description: "Operational guidance for app visibility strategy, approval configuration, group management, and email notifications."
---

# Best practices

### App visibility strategy

1. **Sync all apps** to get your full Intune catalog
2. **Keep system apps hidden** (dependencies, frameworks, required apps)
3. **Make user-requestable apps visible** (productivity tools, optional software)
4. **Use categories** from Intune to help users find apps

### Approval configuration strategy

| App Type | Recommended Setting |
|----------|---------------------|
| Free productivity tools | No approval required |
| Licensed software | Manager approval |
| Admin/privileged tools | Multi-stage with IT Security |
| Developer tools | Manager + IT approval |

### Group management

With automatic group and assignment creation, the portal handles most group management for you:

1. **Automatic Setup**: When you make an app visible, the portal creates a security group and Intune assignment automatically
2. **Consistent Naming**: Groups follow the pattern `{GroupNamePrefix}{AppName}-{arch}-{locale}-v{version}-Required` (e.g., `AppStore-Microsoft Teams-x64-en-US-v1-0-0-Required`). Dots in version numbers are replaced with dashes.
3. **Custom Prefix**: Configure the Group Name Prefix in Settings to match your organization's naming conventions
4. **Manual Override**: You can still manually set a Target Group on an app if you prefer to use an existing group

!!! tip
    To use existing groups instead of auto-created ones, set the Target Group before making the app visible.

### Email notifications

1. Create a dedicated shared mailbox for notifications
2. Grant the app `Mail.Send` permission on that mailbox
3. Use a recognizable From address like `apprequest@company.com`
4. Include your portal URL so users can open it to view status
