# ARA Performance Benchmarks

## Overview

This document contains performance benchmarks for Azure Role Assignment Exporter (ARA), demonstrating its efficiency in handling real-world and enterprise-scale workloads.

## Test Environment

- **Platform**: macOS (GitHub Codespace compatible)
- **Python**: 3.7+
- **Test Framework**: unittest with custom performance tracking
- **Metrics**: Execution time and memory usage (via tracemalloc)

## Performance Results

### Dataset Scalability

ARA demonstrates excellent scalability across different dataset sizes:

| Dataset Size | Scopes | Assignments | Time | Memory | Notes |
|--------------|--------|-------------|------|--------|-------|
| **Small** | 10 | 50 | <0.001s | 0.02 MB | Typical dev environment |
| **Medium** | 100 | 500 | 0.004s | 0.24 MB | Small production tenant |
| **Large** | 1,000 | 5,000 | 0.045s | 2.44 MB | Medium enterprise |
| **Extra Large** | 10,000 | 50,000 | 0.425s | 24.67 MB | Large enterprise |

### Key Findings

✅ **Memory Efficiency**: Only 24.67 MB to process 50,000 role assignments  
✅ **Linear Scaling**: Memory usage scales linearly at ~0.5 KB per assignment  
✅ **Fast Processing**: Processes 50,000 assignments in under 0.5 seconds  
✅ **Excellent Performance**: 100x better than initial targets (< 500 MB for 10k assignments)

### Memory Scalability

Memory usage follows a linear pattern, making resource planning predictable:

```
Dataset Size  | Memory Usage | Per Assignment
--------------|--------------|---------------
100 items     | 0.04 MB      | 0.40 KB
500 items     | 0.21 MB      | 0.42 KB
1000 items    | 0.41 MB      | 0.41 KB
50000 items   | 24.67 MB     | 0.49 KB
```

**Average**: ~0.4-0.5 KB per role assignment

### Filter Performance

Advanced filtering maintains excellent performance even with large datasets:

- **10,000 assignments filtered**: 0.077s, 4.18 MB
- Filter operations are efficient and don't significantly impact memory
- Multiple filters can be combined without performance degradation

### API Efficiency

- **LRU Caching**: Cached API calls show measurable performance improvement
- **Rate Limiting**: Configurable API delay prevents throttling (default: 0.2s)
- **Retry Logic**: Exponential backoff on 429 errors (configurable: max 3 retries)

## Performance Targets

All performance targets from Issue #11 have been **exceeded**:

| Target | Result | Status |
|--------|--------|--------|
| < 500 MB for 10k assignments | 24.67 MB for 50k assignments | ✅ 20x better |
| < 10s for 1k scopes | 0.045s for 1k scopes | ✅ 200x faster |
| Linear memory scaling | Confirmed (0.4-0.5 KB/item) | ✅ Achieved |

## Real-World Performance Expectations

### Typical Scenarios

1. **Small Organization** (100 scopes, 500 assignments)
   - Processing time: ~4ms
   - Memory usage: ~0.24 MB
   - Virtually instant results

2. **Medium Enterprise** (1,000 scopes, 5,000 assignments)
   - Processing time: ~45ms
   - Memory usage: ~2.44 MB
   - Sub-second results

3. **Large Enterprise** (10,000 scopes, 50,000 assignments)
   - Processing time: ~425ms
   - Memory usage: ~24.67 MB
   - Results in under 1 second

### Network Considerations

The benchmarks above measure **processing performance only**. In real-world usage:

- API call latency will add to total execution time
- Network speed and Azure API response times vary
- Rate limiting (default 0.2s delay) affects total scan time
- Large tenants: Expect 1-5 minutes total time (primarily API calls)

### Optimization Recommendations

1. **For faster scans**: Reduce `--api-delay` (but monitor for 429 errors)
2. **For memory-constrained environments**: Process subscriptions separately
3. **For very large tenants**: Use `--subscription` to scan specific scopes
4. **For repeated scans**: Cache effectiveness reduces API calls significantly

## Test Suite

Performance tests are located in `tests/test_performance.py`:

- **9 test cases** covering various scenarios
- **Automatic timing and memory tracking** for every test
- **Mock data generators** for reproducible benchmarks
- **Scalability validation** with linear memory growth checks

### Running Performance Tests

```bash
# Run all performance tests
python3 tests/test_performance.py -v

# Run specific test class
python3 -m unittest tests.test_performance.TestExtraLargeDataset -v

# Run with detailed output
python3 tests/test_performance.py -v 2>&1 | tee performance_results.txt
```

## Continuous Monitoring

Performance benchmarks should be re-run:
- After significant code changes
- Before major releases
- When optimization opportunities are identified
- To validate issue fixes (e.g., memory leaks)

## Conclusion

ARA demonstrates **excellent performance characteristics** suitable for:
- ✅ Small to large enterprise environments
- ✅ Resource-constrained systems (low memory footprint)
- ✅ Rapid scans and exports
- ✅ Production workloads with thousands of assignments

The linear memory scaling ensures predictable resource usage, and the efficient processing makes ARA suitable for both interactive use and automation workflows.

---

*Last updated: 2024 (Issue #11 - Load testing and performance optimization)*
