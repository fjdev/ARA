"""
Edge Case and Error Handling Tests
===================================

Additional tests for edge cases and error conditions.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_utils import get_ara
ara = get_ara()


class TestScopeEdgeCases(unittest.TestCase):
    """Test edge cases in scope handling."""
    
    def test_scope_with_special_characters(self):
        """Test scope with special characters in name."""
        scope = ara.Scope(
            scope_path="/subscriptions/test-123",
            name="Test & Production",
            scope_type="Subscription"
        )
        self.assertEqual(scope.name, "Test & Production")
    
    def test_scope_with_empty_parent(self):
        """Test scope without parent."""
        scope = ara.Scope(
            scope_path="/managementGroups/mg1",
            name="Root MG",
            scope_type="Management Group",
            parent_scope=None
        )
        self.assertIsNone(scope.parent_scope)
    
    def test_scope_with_long_name(self):
        """Test scope with very long name."""
        long_name = "A" * 200
        scope = ara.Scope(
            scope_path="/subscriptions/test",
            name=long_name,
            scope_type="Subscription"
        )
        self.assertEqual(scope.name, long_name)


class TestRoleAssignmentEdgeCases(unittest.TestCase):
    """Test edge cases in role assignment handling."""
    
    def test_assignment_with_unknown_principal(self):
        """Test assignment with Unknown principal name."""
        assignment = ara.RoleAssignment(
            principal_id="deleted-principal-id",
            principal_name="Unknown",
            principal_type="User",
            role_name="Owner",
            role_id="/providers/Microsoft.Authorization/roleDefinitions/owner",
            scope="/subscriptions/test",
            scope_name="Test Subscription",
            scope_type="Subscription"
        )
        self.assertEqual(assignment.principal_name, "Unknown")
    
    def test_assignment_full_scope_path_with_name(self):
        """Test full_scope_path property with scope name."""
        assignment = ara.RoleAssignment(
            principal_id="test-id",
            principal_name="Test",
            principal_type="User",
            role_name="Reader",
            role_id="/providers/Microsoft.Authorization/roleDefinitions/reader",
            scope="/subscriptions/sub1",
            scope_name="Production",
            scope_type="Subscription"
        )
        self.assertIn("Production", assignment.full_scope_path)
        self.assertIn("Subscription", assignment.full_scope_path)
    
    def test_assignment_full_scope_path_without_name(self):
        """Test full_scope_path property without scope name."""
        assignment = ara.RoleAssignment(
            principal_id="test-id",
            principal_name="Test",
            principal_type="User",
            role_name="Reader",
            role_id="/providers/Microsoft.Authorization/roleDefinitions/reader",
            scope="/subscriptions/sub1",
            scope_name="",
            scope_type="Subscription"
        )
        # Should fallback to scope path
        self.assertEqual(assignment.full_scope_path, "/subscriptions/sub1")


class TestValidationErrors(unittest.TestCase):
    """Test validation error handling."""
    
    def test_role_assignment_empty_principal_id(self):
        """Test RoleAssignment rejects empty principal ID."""
        with self.assertRaises(ara.ValidationError):
            ara.RoleAssignment(
                principal_id="",  # Empty
                principal_name="Test",
                principal_type="User",
                role_name="Reader",
                role_id="role-id",
                scope="/subscriptions/test",
                scope_name="Test",
                scope_type="Subscription"
            )
    
    def test_role_assignment_empty_role_name(self):
        """Test RoleAssignment rejects empty role name."""
        with self.assertRaises(ara.ValidationError):
            ara.RoleAssignment(
                principal_id="test-id",
                principal_name="Test",
                principal_type="User",
                role_name="",  # Empty
                role_id="role-id",
                scope="/subscriptions/test",
                scope_name="Test",
                scope_type="Subscription"
            )
    
    def test_role_assignment_empty_scope(self):
        """Test RoleAssignment rejects empty scope."""
        with self.assertRaises(ara.ValidationError):
            ara.RoleAssignment(
                principal_id="test-id",
                principal_name="Test",
                principal_type="User",
                role_name="Reader",
                role_id="role-id",
                scope="",  # Empty
                scope_name="Test",
                scope_type="Subscription"
            )
    
    def test_scope_empty_path(self):
        """Test Scope rejects empty path."""
        with self.assertRaises(ara.ValidationError):
            ara.Scope(
                scope_path="",  # Empty
                name="Test",
                scope_type="Subscription"
            )
    
    def test_scope_empty_name(self):
        """Test Scope rejects empty name."""
        with self.assertRaises(ara.ValidationError):
            ara.Scope(
                scope_path="/subscriptions/test",
                name="",  # Empty
                scope_type="Subscription"
            )
    
    def test_scope_invalid_type(self):
        """Test Scope rejects invalid scope type."""
        with self.assertRaises(ara.ValidationError):
            ara.Scope(
                scope_path="/test",
                name="Test",
                scope_type="InvalidType"  # Not in valid types
            )


class TestExceptionMessages(unittest.TestCase):
    """Test exception messages are informative."""
    
    def test_api_error_message(self):
        """Test APIError preserves message."""
        msg = "API request failed with status 500"
        error = ara.APIError(msg)
        self.assertEqual(str(error), msg)
    
    def test_authentication_error_message(self):
        """Test AuthenticationError preserves message."""
        msg = "Failed to authenticate"
        error = ara.AuthenticationError(msg)
        self.assertEqual(str(error), msg)
    
    def test_export_error_message(self):
        """Test ExportError preserves message."""
        msg = "Failed to export to file"
        error = ara.ExportError(msg)
        self.assertEqual(str(error), msg)
    
    def test_validation_error_message(self):
        """Test ValidationError preserves message."""
        msg = "Invalid input data"
        error = ara.ValidationError(msg)
        self.assertEqual(str(error), msg)


class TestConfigConstants(unittest.TestCase):
    """Test configuration constants are reasonable."""
    
    def test_timeout_is_positive(self):
        """Test API timeout is positive."""
        self.assertGreater(ara.ARAConfig.API_REQUEST_TIMEOUT, 0)
    
    def test_retry_delay_is_positive(self):
        """Test retry delay is positive."""
        self.assertGreater(ara.ARAConfig.RATE_LIMIT_RETRY_DELAY, 0)


if __name__ == '__main__':
    unittest.main()
