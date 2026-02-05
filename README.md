# Azure Role Assignment Exporter (ARA)

[![Version](https://img.shields.io/badge/version-2.1.0-green.svg)](https://github.com/fjdev/ara)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional tool for exporting Azure role assignments at management group and subscription scopes with comprehensive reporting, PIM (Privileged Identity Management) integration, and multiple output formats.

## ✨ Features

- **PIM Integration**: Distinguishes between active permanent, active time-bound, eligible permanent, and eligible time-bound assignments
- **Multiple Authentication Methods**: Environment variables, Azure CLI, macOS Keychain, interactive prompt
- **Multi-Level Scanning**: Management groups, subscriptions, resource groups, and individual resources
- **Flexible Depth Control**: Scan only what you need with configurable depth levels
- **Direct Assignment Filtering**: Only exports direct assignments (excludes inherited)
- **Principal Name Resolution**: Automatic lookup via Microsoft Graph API with "Unknown" fallback
- **Resource Type Filtering**: Focus on specific resource types (VMs, Storage, etc.)
- **Performance Safeguards**: Rate limiting, max resource limits, and API retry logic
- **Multiple Output Formats**: JSON and CSV with structured data
- **Enhanced Filtering**: Filter by role, principal type, principal name (regex), assignment type, or exclude system identities
- **Progress Tracking**: Visual progress bar for long-running scans with ETA
- **Comprehensive Reporting**: Detailed console summaries with PIM statistics
- **Robust Error Handling**: Graceful handling of API errors and permissions
- **Production Ready**: Proper logging, validation, and OOP design
- **Zero Dependencies**: Built entirely with Python standard library

## 🚀 Quick Start

### Installation

```bash
# Download or clone the repository
cd ara

# Make executable
chmod +x ara

# Ready to use!
```

### Basic Usage

```bash
# Scan management group only (default depth)
./ara --scope my-mg

# Scan a specific subscription (auto-detects GUID format)
./ara --scope xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Export to CSV format
./ara --scope my-mg --format csv

# Scan including subscriptions (management group scope only)
./ara --scope my-mg --depth subscriptions

# Scan including resource groups
./ara --scope my-mg --depth resource-groups

# Scan subscription's resource groups
./ara --scope xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx --depth resource-groups

# Scan including individual resources (use with caution on large environments)
./ara --scope my-mg --depth resources --max-resources 1000

# Filter specific resource types
./ara --scope my-mg --depth resources \
  --resource-types Microsoft.Compute/virtualMachines Microsoft.Storage/storageAccounts

# Slow down API calls to avoid rate limiting
./ara --scope my-mg --api-delay 0.5

# Debug mode for troubleshooting
./ara --scope my-mg --debug
```

## 📋 Requirements

- **Python 3.7+**
- **Azure Access Token** with permissions to:
  - Read role assignments (`Microsoft.Authorization/roleAssignments/read`)
  - Read management groups (`Microsoft.Management/managementGroups/read`)
  - Read Microsoft Graph API (for principal name resolution)
  - **Optional (for PIM)**: Read PIM eligible assignments (`Microsoft.Authorization/roleEligibilityScheduleInstances/read`)
  - **Optional (for PIM)**: Read PIM time-bound assignments (`Microsoft.Authorization/roleAssignmentScheduleInstances/read`)
- **Network Access** to Azure Management API and Microsoft Graph API

**Note**: PIM integration is enabled by default. If PIM permissions are not available, ARA will gracefully fall back to standard RBAC data (active permanent assignments only). Use `--skip-pim` to explicitly disable PIM API calls.

## 🔐 Authentication

ARA supports multiple authentication methods, tried in order of preference:

1. **Command Line Token**: `--token YOUR_TOKEN`
2. **Environment Variables**: `AZURE_ACCESS_TOKEN`, `AZURE_TOKEN`, `ARM_ACCESS_TOKEN`
3. **Azure CLI**: Automatic token retrieval via `az account get-access-token`
4. **macOS Keychain**: Stored credentials for repeated use
5. **Interactive Prompt**: Secure token entry with optional keychain storage

### Setting Up Authentication

#### Option 1: Azure CLI (Recommended for Development)
```bash
# Login with Azure CLI
az login

# ARA will automatically use Azure CLI credentials
./ara --scope /providers/Microsoft.Management/managementGroups/my-mg
```

#### Option 2: Environment Variable
```bash
# Get an access token
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

# Set environment variable
export AZURE_ACCESS_TOKEN="$TOKEN"

# Run ARA
./ara --scope /providers/Microsoft.Management/managementGroups/my-mg
```

#### Option 3: Direct Token
```bash
# Get token
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

# Use directly
./ara --scope my-mg --token "$TOKEN"
```

## 🎯 Scope Formats

ARA accepts both management group and subscription scopes in multiple flexible formats:

### Management Group Scopes

```bash
# Simple format (recommended)
./ara --scope my-mg

# Short format
./ara --scope managementGroups/my-mg

# Full Azure path format
./ara --scope /providers/Microsoft.Management/managementGroups/my-mg
```

### Subscription Scopes

```bash
# Subscription GUID (recommended)
./ara --scope xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Short format
./ara --scope subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Full Azure path format
./ara --scope /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Note**: When using subscription scope:
- Default depth automatically changes to `resource-groups`
- The `subscriptions` depth is not available (scope is already a subscription)
- The `management-groups` depth is not available (subscriptions don't contain management groups)
- Valid depths: `resource-groups` or `resources`

## 📊 Output

### File Structure
ARA generates output files in the `results/` directory:

```
results/
├── role_assignments_my-mg.json    # JSON output
└── role_assignments_my-mg.csv     # CSV output
```

### JSON Output Format
```json
```json
{
  "metadata": {
    "tool": "Azure Role Assignment Exporter (ARA)",
    "version": "2.0.0",
    "scan_timestamp": "2026-01-29T10:30:00.000000",
    "scope": "/providers/Microsoft.Management/managementGroups/my-mg",
    "total_scopes_scanned": 15,
    "total_assignments_found": 42
  },
  "role_assignments": [
    {
      "principal_id": "12345678-1234-1234-1234-123456789abc",
      "principal_name": "John Doe",
      "principal_type": "User",
      "role_name": "Owner",
      "scope": "/providers/Microsoft.Management/managementGroups/my-mg",
      "scope_name": "my-mg",
      "scope_type": "Management Group",
      "resource_type": null,
      "assignment_type": "Active permanent",
      "start_date_time": null,
      "end_date_time": null
    },
    {
      "principal_id": "87654321-4321-4321-4321-123456789abc",
      "principal_name": "App Service Principal",
      "principal_type": "ServicePrincipal",
      "role_name": "Contributor",
      "scope": "/subscriptions/.../resourceGroups/rg-prod/providers/Microsoft.Compute/virtualMachines/vm-web-01",
      "scope_name": "vm-web-01",
      "scope_type": "Resource",
      "resource_type": "Microsoft.Compute/virtualMachines",
      "assignment_type": "Eligible permanent",
      "start_date_time": null,
      "end_date_time": null
    }
  ]
}
```

### CSV Output Format
```csv
Name,Principal ID,Type,Role,Scope,Scope Type,Assignment Type,Resource Type,Start Date,End Date
John Doe,12345678-1234-1234-1234-123456789abc,User,Owner,my-mg,Management Group,Active permanent,,,
App Service Principal,87654321-4321-4321-4321-123456789abc,ServicePrincipal,Contributor,vm-web-01,Resource,Eligible permanent,Microsoft.Compute/virtualMachines,,
Unknown,a1b2c3d4-...,ServicePrincipal,Reader,storage-prod,Resource,Active time-bound,Microsoft.Storage/storageAccounts,2026-01-29T10:00:00Z,2026-01-29T18:00:00Z
```

**Note**: "Unknown" appears for deleted/orphaned principals that couldn't be resolved via Graph API.

### Console Summary
```
================================================================================
📋 SUMMARY: Found 42 role assignments across 15 scopes
================================================================================

👤 Role: Contributor (18 assignments)
------------------------------------------------------------
   • Jane Smith (User)
     Scope: Production Subscription (Subscription)
   ... and 16 more

👤 Role: Owner (12 assignments)
------------------------------------------------------------
   • John Doe (User)
     Scope: my-mg (Management Group)
   ... and 10 more
```

## 🔧 Advanced Usage

### Scan Depth Levels

ARA supports four depth levels to control how deep the scan goes:

#### 1. Management Groups Only (Default - `management-groups`)
Scans only management group hierarchies, no subscriptions:
```bash
./ara --scope my-mg --depth management-groups
# Or simply (default):
./ara --scope my-mg
```

#### 2. Subscriptions (`subscriptions`)
Scans management groups and all subscriptions:
```bash
./ara --scope my-mg --depth subscriptions
```

#### 3. Resource Groups (`resource-groups`)
Scans management groups, subscriptions, AND resource groups:
```bash
./ara --scope my-mg --depth resource-groups
```
⚠️ **Performance**: Can take several minutes for environments with many resource groups.

#### 4. Individual Resources (`resources`)
Scans everything including individual resources (VMs, storage accounts, etc.):
```bash
./ara --scope my-mg --depth resources \
  --max-resources 5000 --api-delay 0.3
```
⚠️ **Performance**: Can take significant time for large environments. Use `--max-resources` to limit scope.

### Resource Type Filtering

Focus on specific Azure resource types when using `--depth resources`:

```bash
# Only VMs
./ara --scope my-mg --depth resources \
  --resource-types Microsoft.Compute/virtualMachines

# VMs and Storage Accounts
./ara --scope my-mg --depth resources \
  --resource-types Microsoft.Compute/virtualMachines Microsoft.Storage/storageAccounts

# All network resources
./ara --scope my-mg --depth resources \
  --resource-types Microsoft.Network/virtualNetworks Microsoft.Network/networkSecurityGroups
```

### Performance Tuning

#### Rate Limiting
Control API call frequency to avoid throttling:
```bash
# Default: 0.1 seconds between API calls
./ara --scope my-mg

# Slower (safer for large scans)
./ara --scope my-mg --api-delay 0.5

# Faster (risk of rate limiting)
./ara --scope my-mg --api-delay 0.05
```

ARA automatically implements:
- **Exponential backoff** on HTTP 429 (rate limited) responses
- **Automatic retry** up to 3 attempts with increasing delays
- **Caching** to minimize duplicate API calls

#### Resource Limits
Protect against runaway scans:
```bash
# Limit to 1000 resources
./ara --scope my-mg --depth resources --max-resources 1000

# Default limit (10,000 resources)
./ara --scope my-mg --depth resources
```

### Output Format Options

```bash
# JSON output (default)
./ara --scope my-mg

# CSV output
./ara --scope my-mg --format csv
```

### Progress Tracking

ARA shows a progress bar for long-running scans to track completion and estimate remaining time.

**Features:**
- Real-time progress percentage and ETA
- Scope count (processed/total)
- Processing rate (scopes per second)
- Simple built-in text display

**Usage:**
```bash
# Default: progress bar enabled
./ara --scope my-mg --depth resources

# Disable progress bar
./ara --scope my-mg --no-progress
```

**Display:**
- Built-in progress: `Scanning scopes: [████████████████████] 156/156 (100%) | ETA: 0s | 1.4 scopes/s`
- Debug mode: Progress automatically disabled to show detailed logs

**Note**: Progress is automatically disabled in `--debug` mode or when using `--no-progress`.

### Enhanced Filtering

ARA supports advanced filtering to focus on specific role assignments:

#### Role Filter

Filter by role name (comma-separated for multiple):

```bash
# Find all Owner assignments
./ara --scope my-mg --role-filter "Owner"

# Multiple roles
./ara --scope my-mg --role-filter "Owner,Contributor,Reader"
```

#### Principal Type Filter

Filter by principal type (User, Group, ServicePrincipal):

```bash
# Only service principals
./ara --scope my-mg --principal-type-filter "ServicePrincipal"

# Users and groups only
./ara --scope my-mg --principal-type-filter "User,Group"
```

#### Principal Name Filter

Filter by principal name using regex patterns:

```bash
# Service principals starting with "sp-"
./ara --scope my-mg --principal-name-filter "^sp-.*"

# Admins
./ara --scope my-mg --principal-name-filter ".*admin.*"

# Specific naming pattern
./ara --scope my-mg --principal-name-filter "^(dev|test|prod)-.*"
```

#### Exclude System Identities

Exclude system-assigned managed identities:

```bash
./ara --scope my-mg --exclude-system
```

#### Combined Filters

Filters can be combined for powerful queries:

```bash
# Find all Owner or Contributor service principals
./ara --scope my-mg --role-filter "Owner,Contributor" --principal-type-filter "ServicePrincipal"

# Find admin users with elevated roles
./ara --scope my-mg --principal-name-filter ".*admin.*" --principal-type-filter "User" --role-filter "Owner,Contributor"

# Security audit: Find all users with Owner role, excluding system accounts
./ara --scope my-mg --role-filter "Owner" --principal-type-filter "User" --exclude-system
```

**Features:**
- **Post-processing**: Filters are applied after fetching (all assignments are retrieved, then filtered)
- **Case-insensitive**: All text matching is case-insensitive
- **Regex support**: Principal name filter supports full regex patterns
- **Metadata tracking**: Applied filters are documented in JSON/CSV outputs
- **Count reporting**: Shows both total found and filtered counts in logs

**Use Cases:**
- **Security audits**: Find all Owner assignments across your organization
- **Cleanup operations**: Identify unused service principal assignments
- **Compliance reporting**: Filter specific principal types or roles
- **Investigation**: Search for assignments by naming patterns

### PIM Integration (Privileged Identity Management)

ARA v2.0.0 includes full integration with Azure PIM, distinguishing between four types of role assignments:

1. **Active permanent** - Standard RBAC assignments with no expiration
2. **Active time-bound** - PIM-activated assignments with an end date
3. **Eligible permanent** - PIM-eligible assignments that can be activated anytime
4. **Eligible time-bound** - PIM-eligible assignments with an expiration date

#### How PIM Integration Works

- **Enabled by default**: PIM APIs are called automatically for management groups, subscriptions, and resource groups
- **Graceful fallback**: If PIM permissions are unavailable, ARA continues with standard RBAC data (active permanent only)
- **Resource scope limitation**: PIM is not supported for individual resources per Microsoft documentation
- **Assignment dates**: Start and end dates are included for time-bound assignments

#### PIM Filtering Examples

```bash
# Find all PIM-eligible assignments (identify who can elevate privileges)
./ara --scope my-mg --assignment-type-filter "Eligible permanent,Eligible time-bound"

# Find only permanent assignments (active or eligible)
./ara --scope my-mg --assignment-type-filter "Active permanent,Eligible permanent"

# Security audit: Find all active Owner assignments (permanent + time-bound)
./ara --scope my-mg --role-filter "Owner" --assignment-type-filter "Active permanent,Active time-bound"

# Compliance check: Find all time-bound assignments (PIM-activated or expiring eligible)
./ara --scope my-mg --assignment-type-filter "Active time-bound,Eligible time-bound"

# Disable PIM scanning (faster, useful when PIM not available)
./ara --scope my-mg --skip-pim
```

#### PIM Output Format

All output formats (JSON and CSV) include PIM fields:

**JSON:**
```json
{
  "principal_id": "...",
  "principal_name": "John Doe",
  "role_name": "Contributor",
  "assignment_type": "Eligible permanent",
  "start_date_time": null,
  "end_date_time": null
}
```

**CSV Columns:**
- `Assignment Type`: "Active permanent", "Active time-bound", "Eligible permanent", or "Eligible time-bound"
- `Start Date`: ISO 8601 timestamp (for time-bound assignments)
- `End Date`: ISO 8601 timestamp (for time-bound assignments)

#### PIM Troubleshooting

**PIM data not showing:**
- Verify your account has the required PIM read permissions (see Requirements section)
- Check if PIM is enabled for your tenant
- Use `--debug` to see PIM API call details
- PIM only works for management groups, subscriptions, and resource groups (not individual resources)

**Permission errors:**
- ARA will gracefully fall back to standard RBAC if PIM permissions are unavailable
- All assignments will show as "Active permanent" in fallback mode
- Consider using `--skip-pim` to explicitly disable PIM calls and improve performance

### Debug Mode

```bash
./ara --scope my-mg --debug
```

## 🛠️ Troubleshooting

### Common Issues

**Authentication Failed**
```bash
# Verify Azure CLI is logged in
az account show

# Get a fresh token manually
az account get-access-token --resource https://management.azure.com

# Use debug mode to see authentication flow
./ara --scope my-mg --debug
```

**Permission Denied**
- Ensure your account has `Microsoft.Authorization/roleAssignments/read` permission
- Verify access to the management group scope
- For Graph API name resolution, ensure `User.Read.All` or `Directory.Read.All` permission

**Network Errors**
- Check internet connection
- Verify access to `management.azure.com` and `graph.microsoft.com`
- Try again with `--debug` for detailed error messages

**Rate Limiting (HTTP 429)**
- ARA automatically retries with exponential backoff
- Increase `--api-delay` to slow down requests: `--api-delay 0.5`
- Reduce `--max-resources` for resource-level scans

**Slow Performance**
- Use appropriate `--depth` level (default `subscriptions` is fastest)
- Limit resource scans with `--max-resources`
- Use `--resource-types` to filter specific resource types
- Increase `--api-delay` slightly if getting throttled

**"Unknown" Principals**
- Deleted or orphaned security principals show as "Unknown"
- This matches Azure Portal behavior
- The GUID is preserved in the `Principal ID` column for reference

## ⚡ Performance

ARA is designed for **enterprise-scale performance**:

- **Memory Efficient:** ~0.49 KB per role assignment (linear scaling)
- **Fast Processing:** 50,000 assignments in 0.42 seconds
- **Scalable:** Handles environments from 10 to 100,000+ assignments
- **Optimized Caching:** LRU cache for repeated API calls
- **Smart Rate Limiting:** Configurable delays and automatic retry with exponential backoff

### Performance Benchmarks

| Dataset Size | Scopes | Assignments | Time | Memory |
|--------------|--------|-------------|------|--------|
| Small | 10 | 50 | <0.001s | 0.02 MB |
| Medium | 100 | 500 | 0.004s | 0.24 MB |
| Large | 1,000 | 5,000 | 0.044s | 2.44 MB |
| Enterprise | 10,000 | 50,000 | 0.420s | 24.67 MB |

See [PERFORMANCE.md](PERFORMANCE.md) for detailed benchmarks and analysis.

### Approximate Scan Times

Real-world scan times (includes API latency and network):

| Depth Level | Scopes Scanned | Typical Time | Use Case |
|-------------|----------------|--------------|----------|
| `management-groups` | 1-50 MGs | < 1 minute | Organizational structure audit |
| `subscriptions` | 1-100 subs | 1-3 minutes | Standard RBAC audit |
| `resource-groups` | 100-500 RGs | 3-10 minutes | Detailed subscription audit |
| `resources` | 1000-10000 resources | 10-60 minutes | Complete environment scan |

**Tips for Large Environments**:
- Start with `--depth subscriptions` to get baseline
- Use `--resource-types` to focus on critical resources
- Run resource scans during off-hours
- Consider scanning individual subscriptions separately
- Use `--max-resources` as a safety limit

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**fjdev** - [GitHub](https://github.com/fjdev)

## 🔗 Related Tools

- **TMVS** (Terraform Module Version Scanner) - Scan Terraform Cloud private registry modules
- **UTMS** (Universal Terraform Module Scanner) - Scan repositories for Terraform module usage

Part of the VCC (Version Control & Compliance) Toolkit.

---

**ARA v2.0.0** - Making Azure role assignment auditing with PIM integration simple and professional. 🚀
