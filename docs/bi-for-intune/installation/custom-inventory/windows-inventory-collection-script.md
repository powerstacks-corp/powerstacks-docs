---
title: "Windows Inventory Collection Script"
render_macros: false
---

# Windows Inventory Collection Script

Many customers have asked for reporting on properties that Intune either doesn't collect or doesn't surface accurately. The Windows inventory collection script fills those gaps by gathering hardware, software, driver, monitor, disk, battery, Microsoft 365, and warranty data from each Windows endpoint and sending it to your Azure Log Analytics workspace via the Log Ingestion API. From there, the data flows into the BI for Intune Power BI reports.

## Prerequisites

Before configuring the script, complete these steps:

1. [Create an Entra Application](create-inventory-app-registration.md)
2. [Deploy Azure Resources](deploy-custom-inventory-resources.md)

You should have recorded: Tenant ID, Client ID, Client Secret, DceURI, and DcrImmutableId.

For warranty collection (optional), you'll also need API credentials from each vendor whose devices you want to look up:

- **Dell** — apply at [Dell TechDirect](https://techdirect.dell.com/Portal/APIs.aspx) for a Client ID and Client Secret.
- **Lenovo** — contact your Lenovo account representative to request a Client ID. There is no self-service portal.
- **HP** — sign up at [HP Developer Portal](https://developers.hp.com/) or work with your HP rep for a Client ID and Client Secret. Note that HP secrets expire frequently and need to be refreshed regularly.
- **Getac** — contact your Getac account representative to request API credentials.

## Get the script

The script is hosted on GitHub. Download `Intune_Windows_Inventory.ps1` from the repository:

[![github mark2](../../images/github-mark2-80x80.png)](https://github.com/powerstacks-corp/Windows-Custom-Inventory)

*[Windows Custom Inventory repository](https://github.com/powerstacks-corp/Windows-Custom-Inventory)*

## Configure the script

Update the following settings near the top of the script:

| Parameter | Value |
| --- | --- |
| `LogAPIMode` | `LogIngestionAPI` |
| `TenantId` | Your Directory (Tenant) ID |
| `ClientId` | Your Application (Client) ID |
| `ClientSecret` | Your Client Secret value |
| `DceURI` | From deployment outputs |
| `DcrImmutableId` | From deployment outputs |

### Collection toggles

Each major inventory category can be turned on or off independently. The defaults work for most BI for Intune deployments; adjust if you need to limit what's collected.

| Variable | Description | Default |
| --- | --- | --- |
| `CollectDeviceInventory` | Hardware inventory (CPU, memory, disks, monitors, chassis, OS install date, battery) | `$true` |
| `CollectAppInventory` | Installed Win32 applications | `$true` |
| `CollectDriverInventory` | Installed and optional drivers | `$true` |
| `CollectMicrosoft365` | Microsoft 365 update channel and compliance — sub-toggle of device inventory | `$true` |
| `CollectWarranty` | Warranty lookups via Dell / HP / Lenovo / Getac APIs — sub-toggle of device inventory | `$false` |
| `CollectUWPInventory` | UWP (modern app) inventory in addition to Win32 — sub-toggle of app inventory | `$false` |
| `MatchDrivers` | Match installed driver packages to PnP devices for richer driver records | `$true` |
| `RemoveBuiltInMonitors` | Exclude internal laptop monitors from monitor inventory | `$false` |
| `WarrantyMaxCacheAgeDays` | Days before cached warranty data is refreshed from the vendor API | `180` |
| `WarrantyForceRefresh` | Ignore the local cache and force a fresh warranty API lookup | `$false` |

### Warranty API credentials

If `CollectWarranty` is enabled, fill in the credentials for whichever vendors you have access to:

```powershell
$WarrantyDellClientID     = "<your Dell client ID>"
$WarrantyDellClientSecret = "<your Dell client secret>"
$WarrantyLenovoClientID   = "<your Lenovo client ID>"
$WarrantyHPClientID       = "<your HP client ID>"
$WarrantyHPClientSecret   = "<your HP client secret>"
```

Vendors you don't supply credentials for are skipped silently — there is no need to comment them out.

## Deploy via Intune

Deploy the inventory script as a **detection script** in an Intune remediation:

1. In the [Intune admin center](https://intune.microsoft.com), go to **Devices** > **Remediations**.
2. Create a new remediation package.
3. Upload `Intune_Windows_Inventory.ps1` as the **detection script**.
4. Set **Run this script using the logged-on credentials** to **No** (the script runs as SYSTEM).
5. Set **Run script in 64-bit PowerShell** to **Yes**.
6. Assign the remediation to your target device groups.
7. Set the schedule to **run once per day**.

The script runs silently on each device and sends inventory data to your Log Analytics workspace.

## Data collected

The script writes to three custom tables in Log Analytics. The tables are created automatically on first ingestion.

### `PowerStacksDeviceInventory_CL`

One row per device per run. Includes a flat envelope (`ComputerName`, `ManagedDeviceID`) and a `DeviceDetails` payload that holds the nested hardware inventory.

**Hardware**

| Field | Source | Notes |
| --- | --- | --- |
| `Memory` | `Win32_PhysicalMemory` | Total physical RAM in bytes |
| `CPUManufacturer` | `Win32_Processor` | |
| `CPUName` | `Win32_Processor` | |
| `CPUMaxClockSpeed` | `Win32_Processor` | MHz |
| `CPUPhysical` | `Win32_ComputerSystem` | Physical CPU package count |
| `CPUCores` | `Win32_Processor` | Physical core count |
| `CPULogical` | `Win32_Processor` | Logical processor count |
| `LastBootTime` | `Win32_OperatingSystem` | UTC ISO 8601 |
| `OSInstallDate` | `Win32_OperatingSystem` | UTC ISO 8601 |
| `DeviceManufacturer` | `Win32_ComputerSystem` | |
| `DeviceModel` | `Win32_ComputerSystem` | Friendly name resolved for Lenovo |
| `BatteryDesignedCapacity` | `Win32_Battery` (BatteryStaticData) | mWh |
| `BatteryFullChargedCapacity` | `Win32_Battery` (BatteryFullChargedCapacity) | mWh — combined with the design capacity to compute battery health |
| `Monitors[]` | `WMIMonitorID` (root\WMI) | Array of monitor objects (see below). Built-in monitors can be excluded with `RemoveBuiltInMonitors`. |
| `PhysicalDisks[]` | `Get-PhysicalDisk` + `Get-StorageReliabilityCounter` + `MSStorageDriver_FailurePredictStatus` | Array of disk objects (see below) |
| `Chassis[]` | `Win32_SystemEnclosure` | Array of chassis type entries (see below) |

**`Monitors[]` per-monitor fields:** `Manufacturer`, `Model`, `SerialNumber`, `WeekOfManufacture`, `YearOfManufacture`.

**`PhysicalDisks[]` per-disk fields:** `Number`, `BusType`, `FirmwareVersion`, `HealthStatus`, `Manufacturer`, `Model`, `Name`, `SerialNumber`, `Size`, `Type`, `SMARTPredictFailure`, `SMARTReason`, `Wear`, `ReadErrorsUncorrected`, `ReadErrorsTotal`, `WriteErrorsUncorrected`, `WriteErrorsTotal`, `Temperature`, `TemperatureMax`.

**`Chassis[]` per-entry fields:** `ChassisTypeCode` (numeric SMBIOS code) and `ChassisTag` (SMBIOS asset tag).

**Microsoft 365** (when `CollectMicrosoft365` is `$true`)

A nested `Microsoft365` object containing:

| Field | Notes |
| --- | --- |
| `InstalledVersion` | Office build currently installed |
| `UpdateChannel` | Monthly, Monthly (Preview), Monthly Enterprise, Semi-Annual, Semi-Annual (Preview), or Beta |
| `LatestReleaseType` | Feature Update, Quality Update, or Security Update |
| `LatestReleaseVersion` | Latest version published for the device's channel |
| `EndOfSupportDate` | End-of-support date for the installed version |
| `ReleaseDate` | Release date of the latest version on the device's channel |
| `ReleaseID` | Office release identifier |

**Warranty** (when `CollectWarranty` is `$true` and a credential is configured for the device's vendor)

A nested `Warranty` object containing:

| Field | Notes |
| --- | --- |
| `ServiceProvider` | Dell, HP, Lenovo, or Getac |
| `ServiceModel` | Vendor-friendly model |
| `ServiceTag` | Service tag / serial number used for the lookup |
| `ServiceLevelDescription` | Vendor's description of the warranty service level |
| `WarrantyStartDate` | |
| `WarrantyEndDate` | |

Warranty data is cached locally per device for `WarrantyMaxCacheAgeDays` (default 180) so each daily run does not call the vendor API.

### `PowerStacksAppInventory_CL`

One row per device per run. Includes the `ComputerName`/`ManagedDeviceID` envelope and an `InstalledApps` payload listing every detected application.

**Per-application fields**

| Field | Notes |
| --- | --- |
| `AppName` | Display name |
| `AppVersion` | Display version |
| `AppPublisher` | Publisher / manufacturer |
| `AppType` | `Win32` or, when `CollectUWPInventory` is `$true`, `UWP` |
| `AppInstallDate` | When the registry recorded the install |
| `AppUninstallString` | The vendor-supplied uninstall command |
| `AppUninstallRegPath` | Source uninstall registry key (system or user hive) |

Both 32-bit and 64-bit Win32 application registry hives are read. User-scope installs are read from the currently logged-on user's hive when one is present.

### `PowerStacksDriverInventory_CL`

One row per device per run. Includes the `ComputerName`/`ManagedDeviceID` envelope and a `ListedDrivers` payload listing both installed drivers and (when `MatchDrivers` is enabled) optional drivers available from Windows Update.

**Per-driver fields**

| Field | Notes |
| --- | --- |
| `WUName` | Windows Update title (when sourced from WU) |
| `DriverName` | Friendly device name |
| `DriverVersion` | |
| `DriverReleaseDate` | UTC ISO 8601 |
| `DriverClass` | Device class (e.g. `Display`, `Net`, `System`) |
| `DriverID` | PnP device ID |
| `DriverHardwareID` | Hardware ID |
| `DriverManufacturer` | |
| `DriverInfName` | Driver INF filename |
| `DriverLocation` | Bus/location string |
| `DriverDescription` | |
| `DriverProvider` | Driver provider name |
| `DriverPublishedOn` | Published date when reported by Windows Update |
| `DriverStatus` | `Installed` for currently bound drivers; `Optional` for available-but-not-installed driver updates |

Microsoft-provided drivers are filtered out so the inventory focuses on third-party drivers that admins are most likely to need to track.

## Verify data ingestion

After the script has run on at least one device, verify data is flowing:

1. In the Azure Portal, navigate to your **Log Analytics workspace**.
2. Go to **Logs** and run a query against one of the custom tables:

```kusto
PowerStacksDeviceInventory_CL
| take 10
```

If data appears, the pipeline is working.

For deeper troubleshooting, run the **LogIngestionAPI_CheckDCR** PowerShell script from the [EnhancedInventoryDeploy repository](https://github.com/powerstacks-corp/EnhancedInventoryDeploy). This script retrieves and displays the full DCR configuration, which is useful for diagnosing ingestion issues.

## Next step

If you also manage macOS devices, configure the [macOS Inventory Collection Script](macos-inventory-collection-script.md).
