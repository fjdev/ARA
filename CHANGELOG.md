# Changelog

All notable changes to Azure Role Assignment Exporter (ARA) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-29

### ⚠️ BREAKING CHANGES

**All output formats (JSON, CSV, Excel) have been updated with new fields. Users parsing output programmatically must update their code.**

#### New Fields in All Output Formats:
- **`assignment_type`** (string): Assignment type with four possible values:
  - `"Active permanent"` - Standard RBAC assignment with no expiration
  - `"Active time-bound"` - PIM-activated assignment with an end date
  - `"Eligible permanent"` - PIM-eligible assignment (can be activated anytime)
  - `"Eligible time-bound"` - PIM-eligible assignment with an expiration date
  
- **`start_date_time`** (nullable string): ISO 8601 timestamp for time-bound assignments (null for permanent assignments)

- **`end_date_time`** (nullable string): ISO 8601 timestamp for time-bound assignments (null for permanent assignments)

#### Migration Guide:

**For JSON consumers:**
```diff
{
  "principal_id": "...",
  "principal_name": "...",
  "role_name": "...",
+ "assignment_type": "Active permanent",
+ "start_date_time": null,
+ "end_date_time": null
}
```

**For CSV consumers:**
- Old columns: `Name, Principal ID, Type, Role, Scope, Scope Type, Resource Type`
- New columns: `Name, Principal ID, Type, Role, Scope, Scope Type, Assignment Type, Resource Type, Start Date, End Date`

**For Excel consumers:**
- Role Assignments sheet has 3 additional columns: `Assignment Type`, `Start Date`, `End Date`
- Summary sheet has new section: "Assignments by Type (PIM)"

### Added

#### PIM (Privileged Identity Management) Integration 🎉
- **Full PIM support** distinguishing between four assignment types (active permanent, active time-bound, eligible permanent, eligible time-bound)
- **Automatic PIM detection** - enabled by default for management groups, subscriptions, and resource groups
- **Graceful fallback** - continues with standard RBAC if PIM permissions unavailable
- **PIM API integration** using Microsoft's official endpoints:
  - `roleEligibilityScheduleInstances` for eligible assignments
  - `roleAssignmentScheduleInstances` for time-bound active assignments
- **Deduplication logic** to prevent counting the same assignment twice
- **Separate exception handling** for better error visibility

#### New CLI Options
- `--skip-pim` flag to explicitly disable PIM API calls (improves performance when PIM not needed)
- `--assignment-type-filter` to filter by assignment type (e.g., `--assignment-type-filter "Eligible permanent,Active time-bound"`)

#### Documentation
- **Comprehensive PIM documentation** in README with examples and troubleshooting
- **Updated requirements** with optional PIM permissions
- **PIM filtering examples** for common security audit scenarios
- **Migration guide** for users upgrading from v1.x

#### Output Enhancements
- **Excel Summary sheet** now includes "Assignments by Type (PIM)" statistics
- **Console logging** shows breakdown by assignment type (e.g., "2 active permanent, 1 eligible permanent")
- **Metadata tracking** for PIM scan status in output files

### Changed
- **Version bumped to 2.0.0** (breaking changes)
- **Module docstring updated** to reflect PIM features and v2.0.0
- **README examples updated** with new PIM output fields
- **AssignmentFilter** now supports filtering by assignment_type

### Fixed
- **Duplicate fields bug** in RoleAssignment dataclass (removed duplicate scope, scope_name, scope_type fields)
- **Better error handling** - split PIM exception handling with warning-level logging for partial failures
- **Improved robustness** - PIM failures no longer silent, properly logged at warning level

### Technical Details
- **Performance**: PIM adds 2 API calls per scope (eligible + time-bound active)
- **Scope limitations**: PIM only works for management groups, subscriptions, and resource groups (not individual resources, per Microsoft documentation)
- **Backward compatibility**: Use `--skip-pim` to maintain v1.x behavior (all assignments marked as "Active permanent")
- **Testing**: All 88 tests passing (79 unit + 9 performance), no regressions
- **Security**: CodeQL scan passed with 0 alerts

---

## [1.0.0] - 2025-11-29

### Initial Release

#### Features
- Multiple authentication methods (environment variables, Azure CLI, macOS Keychain, interactive prompt)
- Multi-level scanning (management groups, subscriptions, resource groups, individual resources)
- Flexible depth control with configurable depth levels
- Direct assignment filtering (excludes inherited assignments)
- Principal name resolution via Microsoft Graph API with "Unknown" fallback
- Resource type filtering for focused scans
- Performance safeguards (rate limiting, max resource limits, API retry logic)
- Multiple output formats (JSON, CSV, Excel/xlsx)
- Enhanced filtering (role, principal type, principal name with regex, exclude system identities)
- Progress tracking with visual progress bar and ETA
- Comprehensive console summaries with statistics
- Robust error handling and graceful API error handling
- Production-ready with proper logging, validation, and OOP design
- Minimal dependencies (core uses Python standard library)
- Comprehensive test suite (88 tests: 79 unit + 9 performance)

#### Output Formats
- **JSON**: Structured data with metadata and role assignments
- **CSV**: Simple tabular format for spreadsheet import
- **Excel**: Multi-sheet workbook with Role Assignments, Summary, and Metadata sheets

#### Performance
- Memory efficient: ~0.49 KB per role assignment
- Fast processing: 50,000 assignments in 0.42 seconds
- Optimized caching with LRU cache
- Smart rate limiting with exponential backoff

[2.0.0]: https://github.com/fjdev/ARA/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/fjdev/ARA/releases/tag/v1.0.0
