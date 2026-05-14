---
title: "Configure Application Settings"
description: "Wire the App Store for Intune backend API and frontend web app to your Entra ID tenant by updating appsettings.json and the .env file."
---

# Configure Application Settings

## Backend API configuration

1. Open `appsettings.json` in the API project

2. Update the following values:
```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "Domain": "yourdomain.onmicrosoft.com",
    "TenantId": "your-tenant-id",
    "ClientId": "your-api-client-id",
    "ClientSecret": "your-client-secret"
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=your-sql-server;Database=AppRequestPortal;..."
  }
}
```

## Frontend configuration

1. Copy `.env.example` to `.env` in the Web project

2. Update the values:
```
REACT_APP_CLIENT_ID=your-frontend-client-id
REACT_APP_TENANT_ID=your-tenant-id
REACT_APP_API_CLIENT_ID=your-api-client-id
REACT_APP_REDIRECT_URI=http://localhost:3000
REACT_APP_API_URL=https://localhost:7001/api
```

## Next step

Continue to [Database Setup](database-setup.md).
