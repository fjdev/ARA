# ARA - Future Improvements & TODO

## 🎯 High Priority

- [x] **Add Excel (.xlsx) output format** ✅ *Completed 2025-11-29*
  - Added openpyxl optional dependency
  - Multi-sheet workbook with formatted tables
  - Sheets: Role Assignments, Summary, Metadata
  - Professional formatting with auto-filters and styling

- [x] **GitHub Actions CI/CD** ⏸️ *Deferred - Issue #2 open*
  - Automated testing on push
  - Version tagging and releases
  - Test coverage reporting

- [x] **Subscription-scoped scanning** ✅ *Completed 2025-11-29*
  - Accepts subscription GUID format (auto-detected)
  - Supports multiple formats: GUID, short, full path
  - Smart depth validation (rejects invalid depths)
  - Auto-adjusts default depth to resource-groups
  - Subscription name resolution via Azure API

## 📊 Medium Priority

- [ ] **Enhanced filtering options**
  - `--role-filter`: Filter by role name (e.g., "Owner", "Contributor")
  - `--principal-type-filter`: Filter by principal type (User, Group, ServicePrincipal)
  - `--principal-name-filter`: Filter by principal name pattern (regex)
  - `--exclude-system`: Exclude system-assigned managed identities

- [ ] **Pagination for large datasets**
  - Some environments may have thousands of assignments
  - Add `--page-size` and `--page` options for paginated output
  - Useful for very large scans

- [ ] **Progress bar for long-running scans**
  - Use `tqdm` library (would add dependency)
  - Or implement simple percentage-based progress in console
  - Show: `Scanning resources... [34/156] 21% (ETA: 2m 15s)`

- [ ] **Caching improvements**
  - Save API responses to disk for offline analysis
  - `--use-cache` and `--cache-dir` options
  - Useful for development and repeated analysis

- [ ] **Comparison mode**
  - Compare two scan results (historical vs current)
  - Show added/removed assignments
  - `ara --compare results/old.json results/new.json`

## 🔧 Low Priority / Nice-to-Have

- [ ] **HTML report output**
  - Interactive HTML dashboard
  - Sortable tables, search functionality
  - Charts showing role distribution

- [ ] **Email notifications**
  - Send scan results via email
  - Useful for scheduled audits
  - `--email-to user@example.com`

- [ ] **Scheduled scanning**
  - Built-in scheduler (cron-like)
  - Or documentation for cron/Windows Task Scheduler setup
  - Automated compliance reports

- [ ] **Inheritance visualization**
  - Show which assignments are inherited vs direct
  - Currently only shows direct, but visualization would be helpful
  - Could be part of HTML report

- [ ] **Multi-tenant support**
  - Scan across multiple Azure AD tenants
  - Useful for MSPs managing multiple customers
  - Requires complex auth handling

- [ ] **REST API mode**
  - Run ARA as a web service
  - HTTP endpoints for triggering scans
  - Webhook support for notifications

## 🧪 Testing & Quality

- [ ] **Increase test coverage to 90%+**
  - Currently: 44 tests covering core functionality
  - Add integration tests with mock Azure API
  - Add performance benchmarking tests

- [ ] **Mock Azure API for integration tests**
  - Test full scan workflow without Azure credentials
  - Useful for CI/CD pipelines
  - Validate output formats thoroughly

- [ ] **Load testing**
  - Test with environments of 10k+ resources
  - Measure memory usage and optimize
  - Validate rate limiting effectiveness

## 📚 Documentation

- [ ] **Video tutorial / demo**
  - Screen recording showing basic usage
  - Upload to YouTube or embed in README

- [ ] **FAQ section in README**
  - Common questions from users
  - Troubleshooting guide expansion

- [ ] **Architecture diagram**
  - Visual representation of tool components
  - Show API flow and data processing

- [ ] **Changelog**
  - Maintain CHANGELOG.md
  - Follow semantic versioning
  - Document breaking changes

## 🔐 Security & Compliance

- [ ] **Security audit**
  - Review token handling
  - Ensure credentials are never logged
  - Add security policy (SECURITY.md)

- [ ] **Compliance reports**
  - Pre-built templates for common compliance frameworks
  - SOC 2, ISO 27001, PCI-DSS mappings
  - Show which assignments violate least-privilege

- [ ] **Sensitive data masking**
  - Option to mask principal IDs in output
  - `--mask-sensitive` flag
  - Useful for sharing reports externally

## 🚀 Performance Optimizations

- [ ] **Parallel API calls**
  - Use async/await for concurrent requests
  - Respect rate limits but maximize throughput
  - Could reduce scan time by 50%+

- [ ] **Smart caching strategy**
  - Cache role definitions globally (rarely change)
  - Cache principal names with TTL
  - Invalidate cache intelligently

- [ ] **Incremental scanning**
  - Only scan resources that changed since last run
  - Requires storing state between runs
  - Massive performance improvement for regular audits

## 🌍 Internationalization

- [ ] **Multi-language support**
  - Currently English only
  - Add i18n for console output
  - Support for localized date/time formats

## 🎨 User Experience

- [ ] **Interactive mode**
  - TUI (Text User Interface) using `rich` or `curses`
  - Select management groups from list
  - Configure options interactively

- [ ] **Configuration file support**
  - `ara.config.yaml` or `.ararc`
  - Store default settings
  - Per-project configurations

- [ ] **Verbose levels**
  - Currently: normal and --debug
  - Add: --quiet, --verbose, --very-verbose
  - Fine-grained control over output

## ✅ Recently Completed

### November 29, 2025
- ✅ **Excel (.xlsx) output format**
  - Multi-sheet workbook with professional formatting
  - Sheets: Role Assignments (with filters), Summary (statistics), Metadata
  - Optional dependency (openpyxl) with graceful error handling
  - Fully documented in README

- ✅ **Subscription-scoped scanning**
  - GUID auto-detection (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
  - Multiple format support (GUID, short, full path)
  - Smart depth validation and auto-adjustment
  - Subscription name resolution (shows display name instead of GUID)
  - Comprehensive documentation and examples

- ✅ **Removed 'both' output format**
  - Simplified to just 'json', 'csv', or 'xlsx'
  - Cleaner UX - users run twice if both formats needed

- ✅ **README corrections**
  - Fixed default depth documentation (management-groups, not subscriptions)
  - Updated all examples to use simple scope format
  - Added Scope Formats section with all 3 formats
  - Updated performance benchmarks

### Earlier Releases
- ✅ Multi-level scanning (management-groups, subscriptions, resource-groups, resources)
- ✅ Flexible scope format (simple: `my-mg`, full: `/providers/...`)
- ✅ Resource type filtering
- ✅ Rate limiting with exponential backoff
- ✅ Display name resolution via Graph API
- ✅ "Unknown" fallback for deleted principals
- ✅ CSV with separate Scope and Scope Type columns
- ✅ JSON with resource_type field
- ✅ Comprehensive test suite (44 tests)
- ✅ Performance safeguards (max-resources, api-delay)
- ✅ Default depth changed to management-groups
- ✅ Enhanced error handling and logging

---

**Note**: Items marked with "requires dependency" would break the current zero-dependency design philosophy. Consider carefully before implementing.
