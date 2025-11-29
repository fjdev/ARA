# ARA - Future Improvements & TODO

## 🎯 High Priority

- [ ] **GitHub Actions CI/CD** - Issue #2 open
  - Automated testing on push
  - Version tagging and releases
  - Test coverage reporting

## 📊 Medium Priority

GitHub Issues created for these items - see https://github.com/fjdev/ARA/issues

## ✅ Recently Completed

### November 29, 2025

- ✅ **Load testing and performance optimization** - Issue #11 closed
  - Comprehensive performance test suite (9 tests)
  - Benchmarks for small to enterprise-scale datasets (10 to 50,000 assignments)
  - Memory profiling with `tracemalloc`
  - Performance validation: 50,000 assignments in 0.42s using 24.67 MB
  - Linear memory scaling confirmed (~0.49 KB per assignment)
  - Filter performance: 10,000 assignments in 77ms
  - Cache performance validated
  - Rate limiting configuration tests
  - Detailed performance report (PERFORMANCE.md)
  - **Result:** Exceeds all targets by 20-227x margins

- ✅ **Progress bar for long-running scans** - Issue #6 closed
  - Implemented ProgressTracker class with optional tqdm support
  - Simple text fallback (no dependencies required)
  - Shows percentage, ETA, rate, and scope count
  - Auto-disables in debug mode
  - `--no-progress` flag for manual control
  - Enhanced mode with tqdm: `Scanning scopes: 100%|██████████| 156/156 [01:47<00:00, 1.45scope/s]`
  - Simple mode (built-in): `Scanning scopes: [████████████████████] 156/156 (100%) | ETA: 0s | 1.4 scopes/s`

- ✅ **Enhanced filtering options** - Issue #4 closed
  - `--role-filter`: Filter by role name (comma-separated, case-insensitive)
  - `--principal-type-filter`: Filter by principal type (User, Group, ServicePrincipal)
  - `--principal-name-filter`: Filter by principal name with regex support
  - `--exclude-system`: Exclude system-assigned managed identities
  - All filters combinable for powerful queries
  - Shows both total and filtered counts in logs
  - Filter metadata tracked in JSON/Excel outputs
  - Examples:
    - `./ara --scope my-mg --role-filter "Owner,Contributor"`
    - `./ara --scope my-mg --principal-type-filter "ServicePrincipal"`
    - `./ara --scope my-mg --principal-name-filter "^sp-.*"`

- ✅ **Excel (.xlsx) output format** - Issue #1 closed
  - Multi-sheet workbook with professional formatting
  - Sheets: Role Assignments (with filters), Summary (statistics), Metadata
  - Optional dependency (openpyxl) with graceful error handling
  - Fully documented in README

- ✅ **Subscription-scoped scanning** - Issue #3 closed
  - GUID auto-detection (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
  - Multiple format support (GUID, short, full path)
  - Smart depth validation and auto-adjustment
  - Subscription name resolution (shows display name instead of GUID)
  - Comprehensive documentation and examples

- ✅ **Architectural patterns compliance**
  - ARA follows all VCC Toolkit architectural patterns (100% compliant)
  - Added Filter and ProgressTracker patterns to ARCHITECTURAL_PATTERNS.md
  - 30 classes, 2,117 lines, 44 tests - all within recommended ranges
  - Zero violations, excellent reference implementation

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
- ✅ Comprehensive test suite (88 tests: 79 unit + 9 performance, 100% pass rate)
- ✅ Performance safeguards (max-resources, api-delay)
- ✅ Default depth changed to management-groups
- ✅ Enhanced error handling and logging
- ✅ Optional dependencies with graceful fallbacks (openpyxl, tqdm)

## 🎯 Outstanding GitHub Issues

See https://github.com/fjdev/ARA/issues for remaining open issues:
- **Issue #2**: GitHub Actions CI/CD (deferred)
- **Issue #5**: Pagination for large datasets
- **Issue #7**: Caching improvements  
- **Issue #8**: Comparison mode
- **Issue #9**: Increase test coverage to 90%+ (in progress - 88 tests, est. 85-90% coverage, +66% from baseline)
  - Note: Could improve to 100% by refactoring ara to be importable (enable coverage.py) and adding more edge case tests
- **Issue #10**: Mock Azure API for integration tests

## 🔧 Additional Ideas (Not Yet Issues)

### Low Priority / Nice-to-Have

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

### Testing & Quality

- [ ] **Increase test coverage to 90%+** - Issue #9 in progress
  - Currently: 88 tests (79 unit + 9 performance) covering core functionality
  - Added output handler tests, filter tests, API client tests
  - Additional edge case coverage and integration tests
  - Remaining: Full end-to-end application flow tests

- [ ] **Mock Azure API for integration tests** - Issue #10 open
  - Test full scan workflow without Azure credentials
  - Useful for CI/CD pipelines
  - Validate output formats thoroughly

### Documentation

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

### Security & Compliance

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

### Performance Optimizations

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

### Internationalization

- [ ] **Multi-language support**
  - Currently English only
  - Add i18n for console output
  - Support for localized date/time formats

### User Experience

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

---

**Note**: Items marked with "requires dependency" would break the current zero-dependency design philosophy. Consider carefully before implementing.
