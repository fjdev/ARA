# Azure Role Assignment Exporter (ARA)

[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/fjdev/ara)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional tool for exporting Azure role assignments at management group and subscription scopes with comprehensive reporting and multiple output formats.

## ✨ Features

- **Multiple Authentication Methods**: Environment variables, Azure CLI, macOS Keychain, interactive prompt
- **Multi-Level Scanning**: Management groups, subscriptions, resource groups, and individual resources
- **Flexible Depth Control**: Scan only what you need with configurable depth levels
- **Direct Assignment Filtering**: Only exports direct assignments (excludes inherited)
- **Principal Name Resolution**: Automatic lookup via Microsoft Graph API with "Unknown" fallback
- **Resource Type Filtering**: Focus on specific resource types (VMs, Storage, etc.)
- **Performance Safeguards**: Rate limiting, max resource limits, and API retry logic
- **Multiple Output Formats**: JSON, CSV, and Excel (.xlsx) with structured data and formatting
- **Comprehensive Reporting**: Detailed console summaries with statistics
- **Robust Error Handling**: Graceful handling of API errors and permissions
- **Production Ready**: Proper logging, validation, and OOP design
- **Minimal Dependencies**: Core uses Python standard library (Excel output requires openpyxl)
- **Fully Tested**: Comprehensive test suite with 44+ unit tests

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

# Export to Excel format (requires: pip install openpyxl)
./ara --scope my-mg --format xlsx

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
- **Network Access** to Azure Management API and Microsoft Graph API
- **Optional**: `openpyxl` for Excel output (`pip install openpyxl`)

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
{
  "metadata": {
    "tool": "Azure Role Assignment Exporter (ARA)",
    "version": "1.0.0",
    "scan_timestamp": "2025-11-29T10:30:00.000000",
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
      "resource_type": null
    },
    {
      "principal_id": "87654321-4321-4321-4321-123456789abc",
      "principal_name": "App Service Principal",
      "principal_type": "ServicePrincipal",
      "role_name": "Contributor",
      "scope": "/subscriptions/.../resourceGroups/rg-prod/providers/Microsoft.Compute/virtualMachines/vm-web-01",
      "scope_name": "vm-web-01",
      "scope_type": "Resource",
      "resource_type": "Microsoft.Compute/virtualMachines"
    }
  ]
}
```

### CSV Output Format
```csv
Name,Principal ID,Type,Role,Scope,Scope Type,Resource Type
John Doe,12345678-1234-1234-1234-123456789abc,User,Owner,my-mg,Management Group,
App Service Principal,87654321-4321-4321-4321-123456789abc,ServicePrincipal,Contributor,vm-web-01,Resource,Microsoft.Compute/virtualMachines
Unknown,a1b2c3d4-...,ServicePrincipal,Reader,storage-prod,Resource,Microsoft.Storage/storageAccounts
```

**Note**: "Unknown" appears for deleted/orphaned principals that couldn't be resolved via Graph API.

### Excel Output Format

Excel output generates a multi-sheet workbook with professional formatting:

**Sheet 1: Role Assignments**
- Formatted table with headers, borders, and auto-sized columns
- Frozen header row for easy scrolling
- Auto-filters enabled on all columns
- Same data as CSV with better presentation

**Sheet 2: Summary**
- Total assignment and scope counts
- Assignments grouped by Role
- Assignments grouped by Principal Type
- Assignments grouped by Scope Type

**Sheet 3: Metadata**
- Tool name and version
- Scan timestamp
- Scope scanned
- Total statistics

**Requirements**: Install openpyxl first:
```bash
pip install openpyxl
./ara --scope my-mg --format xlsx
```

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

# Excel output (requires openpyxl)
./ara --scope my-mg --format xlsx
```

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

## ⚡ Performance Benchmarks

Approximate scan times (may vary based on network, API latency, and assignment count):

| Depth Level | Scopes Scanned | Typical Time | Use Case |
|-------------|----------------|--------------|----------|
| `management-groups` (default) | 1-50 MGs | < 1 minute | Organizational structure audit |
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

**ARA v1.0.0** - Making Azure role assignment auditing simple and professional. 🚀
