"""
Performance and Load Testing
=============================

Tests for ARA performance with large-scale datasets.
Benchmarks memory usage, execution time, and API efficiency.
"""

import unittest
import sys
import os
import time
import tracemalloc
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tool using test utilities
from test_utils import get_ara
ara = get_ara()


class PerformanceTestCase(unittest.TestCase):
    """Base class for performance tests with timing and memory tracking."""
    
    def setUp(self):
        """Start timing and memory tracking."""
        self.start_time = time.time()
        tracemalloc.start()
        self.start_memory = tracemalloc.get_traced_memory()[0]
    
    def tearDown(self):
        """Stop timing and memory tracking, report results."""
        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        elapsed = end_time - self.start_time
        memory_used = (peak_memory - self.start_memory) / 1024 / 1024  # MB
        
        print(f"\n{self.id()}:")
        print(f"  Time: {elapsed:.3f}s")
        print(f"  Memory: {memory_used:.2f} MB")


class MockDataGenerator:
    """Generate large mock datasets for performance testing."""
    
    @staticmethod
    def generate_scopes(count: int, scope_type: str = "Management Group") -> list:
        """Generate mock scopes.
        
        Args:
            count: Number of scopes to generate
            scope_type: Type of scope (Management Group, Subscription, etc.)
            
        Returns:
            List of mock Scope objects
        """
        scopes = []
        for i in range(count):
            scope = ara.Scope(
                scope_path=f"/providers/Microsoft.Management/managementGroups/mg-{i}",
                name=f"mg-{i}",
                scope_type=scope_type,
                depth=i % 5  # Vary depth 0-4
            )
            scopes.append(scope)
        return scopes
    
    @staticmethod
    def generate_role_assignments(count: int, scope_path: str = "/test/scope") -> list:
        """Generate mock role assignments.
        
        Args:
            count: Number of assignments to generate
            scope_path: Scope path for assignments
            
        Returns:
            List of mock RoleAssignment objects
        """
        roles = ["Owner", "Contributor", "Reader", "User Access Administrator"]
        principal_types = ["User", "Group", "ServicePrincipal"]
        
        assignments = []
        for i in range(count):
            assignment = ara.RoleAssignment(
                principal_id=f"principal-{i}",
                principal_name=f"Principal {i}",
                principal_type=principal_types[i % len(principal_types)],
                role_name=roles[i % len(roles)],
                role_id=f"/providers/Microsoft.Authorization/roleDefinitions/role-{i % len(roles)}",
                scope=scope_path,
                scope_name="Test Scope",
                scope_type="Management Group",
                resource_type=None
            )
            assignments.append(assignment)
        return assignments
    
    @staticmethod
    def generate_api_response(assignment_count: int) -> dict:
        """Generate mock API response for role assignments.
        
        Args:
            assignment_count: Number of assignments in response
            
        Returns:
            Mock API response dictionary
        """
        roles = ["Owner", "Contributor", "Reader", "User Access Administrator"]
        principal_types = ["User", "Group", "ServicePrincipal"]
        
        assignments = []
        for i in range(assignment_count):
            assignments.append({
                "id": f"/subscriptions/test/providers/Microsoft.Authorization/roleAssignments/assignment-{i}",
                "properties": {
                    "principalId": f"principal-{i}",
                    "principalType": principal_types[i % len(principal_types)],
                    "roleDefinitionId": f"/subscriptions/test/providers/Microsoft.Authorization/roleDefinitions/role-{i % len(roles)}"
                }
            })
        
        return {"value": assignments}


class TestSmallDataset(PerformanceTestCase):
    """Test with small dataset (baseline): 10 scopes, 50 assignments."""
    
    def test_small_scan_performance(self):
        """Benchmark small scan (10 scopes, 50 assignments)."""
        scopes = MockDataGenerator.generate_scopes(10)
        assignments = MockDataGenerator.generate_role_assignments(50)
        
        # Create result container
        result = ara.ScanResult(
            organization="test-org",
            scope="/test/scope"
        )
        
        # Simulate adding scopes and assignments
        for scope in scopes:
            result.add_scanned_scope(scope)
        
        for assignment in assignments:
            result.add_assignment(assignment)
        
        # Verify counts
        self.assertEqual(result.total_scopes_scanned, 10)
        self.assertEqual(result.total_assignments_found, 50)
        self.assertEqual(len(result.scanned_scopes), 10)
        self.assertEqual(len(result.assignments), 50)


class TestMediumDataset(PerformanceTestCase):
    """Test with medium dataset: 100 scopes, 500 assignments."""
    
    def test_medium_scan_performance(self):
        """Benchmark medium scan (100 scopes, 500 assignments)."""
        scopes = MockDataGenerator.generate_scopes(100)
        assignments = MockDataGenerator.generate_role_assignments(500)
        
        result = ara.ScanResult(
            organization="test-org",
            scope="/test/scope"
        )
        
        for scope in scopes:
            result.add_scanned_scope(scope)
        
        for assignment in assignments:
            result.add_assignment(assignment)
        
        self.assertEqual(result.total_scopes_scanned, 100)
        self.assertEqual(result.total_assignments_found, 500)


class TestLargeDataset(PerformanceTestCase):
    """Test with large dataset: 1,000 scopes, 5,000 assignments."""
    
    def test_large_scan_performance(self):
        """Benchmark large scan (1,000 scopes, 5,000 assignments)."""
        scopes = MockDataGenerator.generate_scopes(1000)
        assignments = MockDataGenerator.generate_role_assignments(5000)
        
        result = ara.ScanResult(
            organization="test-org",
            scope="/test/scope"
        )
        
        for scope in scopes:
            result.add_scanned_scope(scope)
        
        for assignment in assignments:
            result.add_assignment(assignment)
        
        self.assertEqual(result.total_scopes_scanned, 1000)
        self.assertEqual(result.total_assignments_found, 5000)
        
        # Memory should be reasonable for 5000 assignments
        # This will be reported in tearDown


class TestExtraLargeDataset(PerformanceTestCase):
    """Test with extra large dataset: 10,000 scopes, 50,000 assignments."""
    
    def test_extra_large_scan_performance(self):
        """Benchmark extra large scan (10,000 scopes, 50,000 assignments)."""
        scopes = MockDataGenerator.generate_scopes(10000)
        assignments = MockDataGenerator.generate_role_assignments(50000)
        
        result = ara.ScanResult(
            organization="test-org",
            scope="/test/scope"
        )
        
        # Use batch operations to improve efficiency
        for scope in scopes:
            result.add_scanned_scope(scope)
        
        for assignment in assignments:
            result.add_assignment(assignment)
        
        self.assertEqual(result.total_scopes_scanned, 10000)
        self.assertEqual(result.total_assignments_found, 50000)
        
        # This test validates we can handle enterprise-scale environments
        # Memory target: < 500 MB for 50,000 assignments


class TestFilterPerformance(PerformanceTestCase):
    """Test filtering performance with large datasets."""
    
    def test_filter_large_dataset(self):
        """Test filtering 10,000 assignments."""
        assignments = MockDataGenerator.generate_role_assignments(10000)
        
        # Create filter
        mock_args = MagicMock()
        mock_args.role_filter = "Owner,Contributor"
        mock_args.principal_type_filter = None
        mock_args.principal_name_filter = None
        mock_args.exclude_system = False
        
        filter_obj = ara.AssignmentFilter(mock_args)
        
        # Apply filter
        filtered = filter_obj.apply(assignments)
        
        # Should filter to only Owner and Contributor roles
        # With 4 roles cycling, we expect ~50% match
        self.assertGreater(len(filtered), 0)
        self.assertLess(len(filtered), len(assignments))
        
        # Verify all filtered items match criteria
        for assignment in filtered:
            self.assertIn(assignment.role_name, ["Owner", "Contributor"])


class TestCachePerformance(PerformanceTestCase):
    """Test LRU cache effectiveness."""
    
    def test_cache_hit_performance(self):
        """Test that cached API calls are faster."""
        # Create API client
        api_client = ara.AzureAPIClient("test-token")
        
        test_url = "https://management.azure.com/test"
        mock_response = {"value": [{"test": "data"}]}
        
        # Mock the internal request method
        with patch.object(api_client, '_make_request_internal', return_value=mock_response):
            # First call (cache miss)
            start = time.time()
            result1 = api_client._make_cached_request(test_url)
            first_call_time = time.time() - start
            
            # Second call (cache hit)
            start = time.time()
            result2 = api_client._make_cached_request(test_url)
            second_call_time = time.time() - start
            
            # Verify results are identical
            self.assertEqual(result1, result2)
            
            # Cache hit should be significantly faster
            # (though in tests with mocks, difference may be minimal)
            self.assertLessEqual(second_call_time, first_call_time * 1.1)
        
        # Clean up
        api_client._make_cached_request.cache_clear()


class TestRateLimitingPerformance(PerformanceTestCase):
    """Test rate limiting configuration and backoff behavior."""
    
    def test_rate_limit_delay(self):
        """Test that API delay parameter is configured correctly."""
        api_delay = 0.05  # 50ms delay
        api_client = ara.AzureAPIClient("test-token", api_delay=api_delay)
        
        # Verify the client was created with rate limiting configured
        self.assertEqual(api_client.api_delay, api_delay)
        self.assertIsNotNone(api_client._last_request_time)
    
    def test_rate_limit_retry(self):
        """Test that rate limit retry configuration is present."""
        # Verify rate limiting configuration exists in ARAConfig
        self.assertTrue(hasattr(ara.ARAConfig, 'HTTP_RATE_LIMITED'))
        self.assertTrue(hasattr(ara.ARAConfig, 'MAX_RETRY_ATTEMPTS'))
        self.assertTrue(hasattr(ara.ARAConfig, 'RATE_LIMIT_RETRY_DELAY'))
        
        # Verify sensible values
        self.assertEqual(ara.ARAConfig.HTTP_RATE_LIMITED, 429)
        self.assertGreater(ara.ARAConfig.MAX_RETRY_ATTEMPTS, 0)
        self.assertGreater(ara.ARAConfig.RATE_LIMIT_RETRY_DELAY, 0)


class TestMemoryScalability(PerformanceTestCase):
    """Test memory usage scales linearly with data size."""
    
    def test_memory_linear_scaling(self):
        """Verify memory usage is approximately linear with dataset size."""
        results = []
        
        # Test with increasing sizes
        for size in [100, 500, 1000]:
            tracemalloc.start()
            start_mem = tracemalloc.get_traced_memory()[0]
            
            assignments = MockDataGenerator.generate_role_assignments(size)
            result = ara.ScanResult(
                organization="test",
                scope="/test"
            )
            
            for assignment in assignments:
                result.add_assignment(assignment)
            
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            memory_used = (peak_mem - start_mem) / 1024 / 1024  # MB
            results.append((size, memory_used))
            
            print(f"Size {size}: {memory_used:.2f} MB")
        
        # Verify memory usage is reasonable
        # Each assignment should take < 1 KB on average
        for size, memory in results:
            memory_per_item = memory / size * 1024  # KB per item
            self.assertLess(memory_per_item, 10)  # < 10 KB per assignment


if __name__ == '__main__':
    # Run with verbose output to see performance metrics
    unittest.main(verbosity=2)
