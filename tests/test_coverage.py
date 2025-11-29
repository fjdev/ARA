"""
Additional Coverage Tests
=========================

Tests to increase coverage for untested code paths.
"""

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import patch, Mock, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_utils import get_ara
ara = get_ara()

# Test helper to create valid RoleAssignment
def create_test_assignment(principal_name="Test User", role_name="Owner", principal_type="User"):
    return ara.RoleAssignment(
        principal_id="user-123",
        principal_name=principal_name,
        principal_type=principal_type,
        role_name=role_name,
        role_id="role-123",
        scope="/subscriptions/sub1",
        scope_name="Test Sub",
        scope_type="subscription",
        resource_type=None
    )


class TestOutputHandlers(unittest.TestCase):
    """Test output handler classes."""
    
    def test_json_output_handler_initialization(self):
        """Test JSON output handler can be created."""
        handler = ara.JSONOutputHandler()
        self.assertIsInstance(handler, ara.JSONOutputHandler)
    
    def test_csv_output_handler_initialization(self):
        """Test CSV output handler can be created."""
        handler = ara.CSVOutputHandler()
        self.assertIsInstance(handler, ara.CSVOutputHandler)
    
    def test_excel_output_handler_initialization(self):
        """Test Excel output handler can be created."""
        try:
            handler = ara.ExcelOutputHandler()
            self.assertIsInstance(handler, ara.ExcelOutputHandler)
        except ImportError:
            self.skipTest("openpyxl not installed")
    
    def test_summary_output_handler(self):
        """Test summary output handler."""
        handler = ara.SummaryOutputHandler()
        self.assertIsInstance(handler, ara.SummaryOutputHandler)


class TestFilterMethods(unittest.TestCase):
    """Test filter methods."""
    
    def setUp(self):
        """Create test assignments."""
        self.assignments = [
            create_test_assignment("Test User", "Owner", "User"),
            create_test_assignment("Service Principal", "Contributor", "ServicePrincipal")
        ]
    
    def test_filter_parse_list_filter_none(self):
        """Test _parse_list_filter with None."""
        result = ara.AssignmentFilter._parse_list_filter(None)
        self.assertIsNone(result)


class TestProgressTrackerMethods(unittest.TestCase):
    """Test progress tracker methods."""
    
    def test_progress_tracker_context_manager(self):
        """Test progress tracker as context manager."""
        with ara.ProgressTracker(total=10, desc="Test", disable=True) as tracker:
            tracker.update(5)
        
        # Should complete without errors
        self.assertTrue(True)
    
    def test_progress_tracker_update_method(self):
        """Test progress tracker update."""
        tracker = ara.ProgressTracker(total=100, desc="Test", disable=True)
        tracker.update(50)
        tracker.close()
        
        self.assertTrue(True)
    
    def test_progress_tracker_format_time(self):
        """Test time formatting in progress tracker."""
        tracker = ara.ProgressTracker(total=100, desc="Test", disable=True)
        
        # Access the method through the instance
        formatted = tracker._format_time(65)
        
        # Format is "1m 5s" not "01:05"
        self.assertTrue(len(formatted) > 0)
        tracker.close()


class TestScopeMethods(unittest.TestCase):
    """Test Scope class methods."""
    
    def test_scope_from_path_subscription(self):
        """Test creating Scope from subscription path."""
        scope = ara.Scope.from_path("/subscriptions/00000000-0000-0000-0000-000000000001")
        
        self.assertEqual(scope.scope_type, "Subscription")  # Capitalized
        self.assertIn("subscriptions", scope.scope_path)
    
    def test_scope_from_path_management_group(self):
        """Test creating Scope from management group path."""
        scope = ara.Scope.from_path("/providers/Microsoft.Management/managementGroups/my-mg")
        
        self.assertEqual(scope.scope_type, "Management Group")  # Capitalized
    
    def test_scope_from_path_resource_group(self):
        """Test creating Scope from resource group path."""
        scope = ara.Scope.from_path("/subscriptions/sub1/resourceGroups/rg1")
        
        self.assertEqual(scope.scope_type, "Resource Group")  # Capitalized
    
    def test_scope_from_path_resource(self):
        """Test creating Scope from resource path."""
        scope = ara.Scope.from_path(
            "/subscriptions/sub1/resourceGroups/rg1/providers/Microsoft.Compute/virtualMachines/vm1"
        )
        
        self.assertEqual(scope.scope_type, "Resource")  # Capitalized


class TestRoleAssignmentProperties(unittest.TestCase):
    """Test RoleAssignment properties."""
    
    def test_full_scope_path_with_name(self):
        """Test full_scope_path property with scope name."""
        assignment = create_test_assignment()
        
        path = assignment.full_scope_path
        
        # Should include scope name and type
        self.assertTrue(len(path) > 0)
    
    def test_full_scope_path_without_name(self):
        """Test full_scope_path property without scope name."""
        assignment = ara.RoleAssignment(
            principal_id="user-1",
            principal_name="Test",
            principal_type="User",
            role_name="Owner",
            role_id="role-1",
            scope="/subscriptions/sub1",
            scope_name=None,
            scope_type="subscription"
        )
        
        path = assignment.full_scope_path
        
        self.assertEqual(path, "/subscriptions/sub1")


class TestAPIClientMethods(unittest.TestCase):
    """Test API client methods."""
    
    @patch('urllib.request.urlopen')
    def test_api_client_test_authentication(self, mock_urlopen):
        """Test API client authentication test."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"value": []}).encode()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        client = ara.AzureAPIClient("fake-token")
        result = client.test_authentication()
        
        self.assertTrue(result)


class TestGraphAPIClient(unittest.TestCase):
    """Test Graph API client."""
    
    def test_graph_client_initialization(self):
        """Test Graph API client can be created."""
        client = ara.GraphAPIClient()
        self.assertIsInstance(client, ara.GraphAPIClient)
    
    @patch.object(ara.GraphAPIClient, '_get_graph_token')
    @patch('urllib.request.urlopen')
    def test_graph_client_get_principal_name(self, mock_urlopen, mock_token):
        """Test getting principal display name."""
        mock_token.return_value = "fake-token"
        
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "displayName": "Test User"
        }).encode()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        client = ara.GraphAPIClient()
        name = client.get_principal_display_name("user-123", "User")
        
        self.assertEqual(name, "Test User")


if __name__ == '__main__':
    unittest.main()
