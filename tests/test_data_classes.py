"""
Data Classes and Core Models Tests
===================================

Tests for ARA data classes including RoleAssignment, Scope, and ScanResult.
"""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARA module using test utilities
from test_utils import get_ara
ara = get_ara()


class TestRoleAssignment(unittest.TestCase):
    """Test RoleAssignment data class."""
    
    def test_role_assignment_creation(self):
        """Test creating a valid RoleAssignment."""
        assignment = ara.RoleAssignment(
            principal_id="user-123",
            principal_name="user@example.com",
            principal_type="User",
            role_name="Contributor",
            role_id="/subscriptions/test-sub/providers/Microsoft.Authorization/roleDefinitions/role-id",
            scope="/subscriptions/test-sub",
            scope_name="Test Subscription",
            scope_type="Subscription"
        )
        
        self.assertEqual(assignment.scope, "/subscriptions/test-sub")
        self.assertEqual(assignment.role_name, "Contributor")
        self.assertEqual(assignment.principal_id, "user-123")
        self.assertEqual(assignment.principal_name, "user@example.com")
        self.assertEqual(assignment.principal_type, "User")
    
    def test_role_assignment_immutable(self):
        """Test that RoleAssignment is immutable (frozen)."""
        assignment = ara.RoleAssignment(
            principal_id="user-123",
            principal_name="user@example.com",
            principal_type="User",
            role_name="Contributor",
            role_id="role-id",
            scope="/subscriptions/test-sub",
            scope_name="Test Subscription",
            scope_type="Subscription"
        )
        
        # Frozen dataclass should raise exception when trying to modify
        with self.assertRaises(Exception):
            assignment.scope = "/new/scope"


class TestScope(unittest.TestCase):
    """Test Scope data class."""
    
    def test_scope_creation(self):
        """Test creating a valid Scope."""
        scope = ara.Scope(
            scope_path="/subscriptions/test-sub",
            name="Test Subscription",
            scope_type="Subscription"
        )
        
        self.assertEqual(scope.scope_path, "/subscriptions/test-sub")
        self.assertEqual(scope.scope_type, "Subscription")
        self.assertEqual(scope.name, "Test Subscription")
    
    def test_scope_validation_invalid_type(self):
        """Test scope validation with invalid type."""
        with self.assertRaises(ara.ValidationError):
            ara.Scope(
                scope_path="/test",
                name="Test",
                scope_type="invalid_type"
            )
    
    def test_scope_validation_valid_types(self):
        """Test scope validation with all valid types."""
        valid_types = ["Management Group", "Subscription"]
        
        for scope_type in valid_types:
            scope = ara.Scope(
                scope_path=f"/test/{scope_type}",
                name=f"Test {scope_type}",
                scope_type=scope_type
            )
            self.assertEqual(scope.scope_type, scope_type)


class TestScanResult(unittest.TestCase):
    """Test ScanResult data class."""
    
    def test_scan_result_creation(self):
        """Test creating a ScanResult."""
        result = ara.ScanResult(
            organization="test-org",
            scope="/subscriptions/test-sub"
        )
        
        self.assertEqual(result.scope, "/subscriptions/test-sub")
        self.assertEqual(result.organization, "test-org")
        self.assertIsInstance(result.scan_timestamp, str)
        self.assertEqual(len(result.assignments), 0)
        self.assertEqual(result.total_assignments_found, 0)
    
    def test_scan_result_add_assignment(self):
        """Test adding assignments to ScanResult."""
        result = ara.ScanResult(
            organization="test-org",
            scope="/subscriptions/test-sub"
        )
        
        assignment = ara.RoleAssignment(
            principal_id="user-123",
            principal_name="user@example.com",
            principal_type="User",
            role_name="Contributor",
            role_id="role-id",
            scope="/subscriptions/test-sub",
            scope_name="Test Subscription",
            scope_type="Subscription"
        )
        
        result.add_assignment(assignment)
        
        self.assertEqual(len(result.assignments), 1)
        self.assertEqual(result.assignments[0], assignment)
    
    def test_scan_result_multiple_assignments(self):
        """Test adding multiple assignments to ScanResult."""
        result = ara.ScanResult(
            organization="test-org",
            scope="/subscriptions/test-sub"
        )
        
        assignments = [
            ara.RoleAssignment(
                principal_id="user-123",
                principal_name="user@example.com",
                principal_type="User",
                role_name="Contributor",
                role_id="role-id-1",
                scope="/subscriptions/test-sub",
                scope_name="Test Subscription",
                scope_type="Subscription"
            ),
            ara.RoleAssignment(
                principal_id="user-456",
                principal_name="admin@example.com",
                principal_type="User",
                role_name="Reader",
                role_id="role-id-2",
                scope="/subscriptions/test-sub",
                scope_name="Test Subscription",
                scope_type="Subscription"
            )
        ]
        
        for assignment in assignments:
            result.add_assignment(assignment)
        
        self.assertEqual(len(result.assignments), 2)


if __name__ == '__main__':
    unittest.main()
