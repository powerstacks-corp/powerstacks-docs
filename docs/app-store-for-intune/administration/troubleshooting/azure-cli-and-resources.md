---
title: "Azure CLI and resources"
description: "Handy Azure CLI commands for App Store for Intune, plus links to related guides."
---

# Azure CLI and resources

## Useful Azure CLI commands

**View App Service configuration**
```bash
az webapp config show \
  --name <your-app-name> \
  --resource-group <your-resource-group>
```

**Restart App Service**
```bash
az webapp restart \
  --name <your-app-name> \
  --resource-group <your-resource-group>
```

**View environment variables**
```bash
az webapp config appsettings list \
  --name <your-app-name> \
  --resource-group <your-resource-group>
```

**View connection strings**
```bash
az webapp config connection-string list \
  --name <your-app-name> \
  --resource-group <your-resource-group>
```

**Check App Service health**
```bash
az webapp show \
  --name <your-app-name> \
  --resource-group <your-resource-group> \
  --query "state"
```

## Related resources

- [Admin guide](../index.md): complete administration documentation
- [Setup guide](../../installation/setup-guide/prerequisites.md): deployment and configuration
- [Security overview](../security.md): security model and compliance
- [Architecture](../architecture.md): design choices and data flows
