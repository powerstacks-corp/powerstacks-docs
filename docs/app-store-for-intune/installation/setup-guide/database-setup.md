---
title: "Database Setup"
description: "Set the connection string and run Entity Framework Core migrations to create the App Store for Intune database schema."
---

# Database Setup

1. Ensure you have SQL Server running locally or use Azure SQL Database
   - **LocalDB** (included with Visual Studio): Connection string uses `(localdb)\MSSQLLocalDB`
   - **SQL Server Express**: Connection string uses `localhost\SQLEXPRESS`
   - **Azure SQL**: Use the full server FQDN from Azure Portal

2. Update the connection string in `appsettings.json`

   Example for LocalDB:
   ```json
   "ConnectionStrings": {
     "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=AppRequestPortal;Trusted_Connection=True;MultipleActiveResultSets=true"
   }
   ```

3. Restore NuGet packages:
```powershell
cd src/AppRequestPortal.API
dotnet restore
```

4. Run database migrations (from the API project directory):
```powershell
dotnet ef migrations add InitialCreate --project ../AppRequestPortal.Infrastructure --startup-project .
dotnet ef database update --project ../AppRequestPortal.Infrastructure --startup-project .
```

> **Note:** The `--project` flag points to where the DbContext lives (Infrastructure), and `--startup-project` points to the API project which has the configuration.

## Next step

Continue to [Configure Admin Access](configure-admin-access.md).
