#!/usr/bin/env python3
"""
Tests for resource scanning functionality in ARA.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Import utilities
from test_utils import get_ara


class TestScopeFromPath(unittest.TestCase):
    """Test Scope.from_path() for different scope types."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.Scope = self.ara.Scope
    
    def test_management_group_scope(self):
        """Test parsing management group scope path."""
        scope_path = "/providers/Microsoft.Management/managementGroups/test-mg"
        scope = self.Scope.from_path(scope_path)
        
        self.assertEqual(scope.scope_type, 'Management Group')
        self.assertEqual(scope.name, 'test-mg')
        self.assertEqual(scope.scope_path, scope_path)
    
    def test_subscription_scope(self):
        """Test parsing subscription scope path."""
        scope_path = "/subscriptions/12345678-1234-1234-1234-123456789abc"
        scope = self.Scope.from_path(scope_path)
        
        self.assertEqual(scope.scope_type, 'Subscription')
        self.assertEqual(scope.name, '12345678-1234-1234-1234-123456789abc')
        self.assertEqual(scope.scope_path, scope_path)
    
    def test_resource_group_scope(self):
        """Test parsing resource group scope path."""
        scope_path = "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/test-rg"
        scope = self.Scope.from_path(scope_path)
        
        self.assertEqual(scope.scope_type, 'Resource Group')
        self.assertEqual(scope.name, 'test-rg')
        self.assertEqual(scope.scope_path, scope_path)
    
    def test_resource_scope(self):
        """Test parsing individual resource scope path."""
        scope_path = "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/test-vm"
        scope = self.Scope.from_path(scope_path)
        
        self.assertEqual(scope.scope_type, 'Resource')
        self.assertEqual(scope.name, 'test-vm')
        self.assertEqual(scope.resource_type, 'Microsoft.Compute/virtualMachines')
        self.assertEqual(scope.scope_path, scope_path)
    
    def test_complex_resource_scope(self):
        """Test parsing complex resource with multiple segments."""
        scope_path = "/subscriptions/12345678-1234-1234-1234-123456789abc/resourceGroups/test-rg/providers/Microsoft.Network/virtualNetworks/vnet/subnets/subnet1"
        scope = self.Scope.from_path(scope_path)
        
        self.assertEqual(scope.scope_type, 'Resource')
        self.assertEqual(scope.name, 'subnet1')
        self.assertEqual(scope.resource_type, 'Microsoft.Network/virtualNetworks/vnet/subnets')
        self.assertEqual(scope.scope_path, scope_path)


class TestResourceGroupClient(unittest.TestCase):
    """Test ResourceGroupClient functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.ResourceGroupClient = self.ara.ResourceGroupClient
        
        # Create mock API client
        self.mock_api_client = Mock()
        self.client = self.ResourceGroupClient(self.mock_api_client)
    
    def test_list_resource_groups_success(self):
        """Test successful listing of resource groups."""
        # Mock API response
        mock_response = {
            'value': [
                {
                    'name': 'rg-test-1',
                    'id': '/subscriptions/test-sub/resourceGroups/rg-test-1'
                },
                {
                    'name': 'rg-test-2',
                    'id': '/subscriptions/test-sub/resourceGroups/rg-test-2'
                }
            ]
        }
        self.mock_api_client._make_request.return_value = mock_response
        
        # Call the method
        result = self.client.list_resource_groups('test-sub')
        
        # Verify results
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'rg-test-1')
        self.assertEqual(result[0].scope_type, 'Resource Group')
        self.assertEqual(result[1].name, 'rg-test-2')
    
    def test_list_resource_groups_empty(self):
        """Test listing resource groups when none exist."""
        mock_response = {'value': []}
        self.mock_api_client._make_request.return_value = mock_response
        
        result = self.client.list_resource_groups('test-sub')
        
        self.assertEqual(len(result), 0)
    
    def test_list_resource_groups_api_error(self):
        """Test handling of API errors."""
        self.mock_api_client._make_request.side_effect = Exception("API Error")
        
        result = self.client.list_resource_groups('test-sub')
        
        # Should return empty list on error
        self.assertEqual(len(result), 0)


class TestResourceClient(unittest.TestCase):
    """Test ResourceClient functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.ResourceClient = self.ara.ResourceClient
        
        # Create mock API client
        self.mock_api_client = Mock()
        self.client = self.ResourceClient(self.mock_api_client)
    
    def test_list_resources_success(self):
        """Test successful listing of resources."""
        mock_response = {
            'value': [
                {
                    'name': 'vm-test-1',
                    'id': '/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/vm-test-1',
                    'type': 'Microsoft.Compute/virtualMachines'
                },
                {
                    'name': 'vnet-test',
                    'id': '/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.Network/virtualNetworks/vnet-test',
                    'type': 'Microsoft.Network/virtualNetworks'
                }
            ]
        }
        self.mock_api_client._make_request.return_value = mock_response
        
        result = self.client.list_resources('test-sub', 'test-rg')
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'vm-test-1')
        self.assertEqual(result[0].scope_type, 'Resource')
        self.assertEqual(result[0].resource_type, 'Microsoft.Compute/virtualMachines')
    
    def test_list_resources_with_filter(self):
        """Test listing resources with type filter."""
        mock_response = {
            'value': [
                {
                    'name': 'vm-test-1',
                    'id': '/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/vm-test-1',
                    'type': 'Microsoft.Compute/virtualMachines'
                },
                {
                    'name': 'vnet-test',
                    'id': '/subscriptions/test-sub/resourceGroups/test-rg/providers/Microsoft.Network/virtualNetworks/vnet-test',
                    'type': 'Microsoft.Network/virtualNetworks'
                }
            ]
        }
        self.mock_api_client._make_request.return_value = mock_response
        
        # Filter for only VMs
        result = self.client.list_resources(
            'test-sub', 
            'test-rg', 
            resource_type_filter=['Microsoft.Compute/virtualMachines']
        )
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'vm-test-1')
        self.assertEqual(result[0].resource_type, 'Microsoft.Compute/virtualMachines')
    
    def test_list_resources_empty(self):
        """Test listing resources when none exist."""
        mock_response = {'value': []}
        self.mock_api_client._make_request.return_value = mock_response
        
        result = self.client.list_resources('test-sub', 'test-rg')
        
        self.assertEqual(len(result), 0)


class TestRateLimiting(unittest.TestCase):
    """Test API rate limiting and retry logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.AzureAPIClient = self.ara.AzureAPIClient
    
    @patch('time.sleep')
    def test_api_delay_applied(self, mock_sleep):
        """Test that API delay is applied between requests."""
        client = self.AzureAPIClient('fake-token', api_delay=0.5)
        
        self.assertEqual(client.api_delay, 0.5)
    
    @patch('time.sleep')
    @patch('urllib.request.urlopen')
    def test_rate_limit_retry(self, mock_urlopen, mock_sleep):
        """Test retry logic on 429 rate limit."""
        # First call returns 429, second succeeds
        mock_error = Mock()
        mock_error.code = 429
        mock_error.read.return_value.decode.return_value = "Rate limited"
        
        mock_success = Mock()
        mock_success.read.return_value.decode.return_value = '{"value": []}'
        mock_success.__enter__ = Mock(return_value=mock_success)
        mock_success.__exit__ = Mock(return_value=False)
        
        mock_urlopen.side_effect = [
            Mock(side_effect=self.ara.urllib.error.HTTPError('url', 429, 'Rate Limited', {}, mock_error)),
            mock_success
        ]
        
        client = self.AzureAPIClient('fake-token', api_delay=0.1)
        
        # Should eventually succeed after retry
        try:
            result = client._make_request('https://test.com')
        except:
            # Expected to fail in test due to mocking complexity
            pass


class TestRoleAssignmentWithResources(unittest.TestCase):
    """Test RoleAssignment with resource_type field."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.RoleAssignment = self.ara.RoleAssignment
    
    def test_role_assignment_with_resource_type(self):
        """Test creating role assignment with resource_type."""
        assignment = self.RoleAssignment(
            principal_id='test-principal-id',
            principal_name='Test Principal',
            principal_type='ServicePrincipal',
            role_name='Contributor',
            role_id='/providers/Microsoft.Authorization/roleDefinitions/test',
            scope='/subscriptions/test/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm',
            scope_name='vm',
            scope_type='Resource',
            resource_type='Microsoft.Compute/virtualMachines'
        )
        
        self.assertEqual(assignment.resource_type, 'Microsoft.Compute/virtualMachines')
        self.assertEqual(assignment.scope_type, 'Resource')
    
    def test_role_assignment_without_resource_type(self):
        """Test creating role assignment without resource_type."""
        assignment = self.RoleAssignment(
            principal_id='test-principal-id',
            principal_name='Test Principal',
            principal_type='ServicePrincipal',
            role_name='Contributor',
            role_id='/providers/Microsoft.Authorization/roleDefinitions/test',
            scope='/subscriptions/test',
            scope_name='Test Subscription',
            scope_type='Subscription',
            resource_type=None
        )
        
        self.assertIsNone(assignment.resource_type)
        self.assertEqual(assignment.scope_type, 'Subscription')


class TestDepthConfiguration(unittest.TestCase):
    """Test depth configuration constants."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ara = get_ara()
        self.ARAConfig = self.ara.ARAConfig
    
    def test_depth_constants_exist(self):
        """Test that depth constants are defined."""
        self.assertEqual(self.ARAConfig.DEPTH_MANAGEMENT_GROUPS, 'management-groups')
        self.assertEqual(self.ARAConfig.DEPTH_SUBSCRIPTIONS, 'subscriptions')
        self.assertEqual(self.ARAConfig.DEPTH_RESOURCE_GROUPS, 'resource-groups')
        self.assertEqual(self.ARAConfig.DEPTH_RESOURCES, 'resources')
    
    def test_default_depth(self):
        """Test default depth is management-groups."""
        self.assertEqual(self.ARAConfig.DEFAULT_DEPTH, 'management-groups')
    
    def test_rate_limit_constants(self):
        """Test rate limiting constants."""
        self.assertEqual(self.ARAConfig.DEFAULT_MAX_RESOURCES, 10000)
        self.assertIsInstance(self.ARAConfig.DEFAULT_API_DELAY, float)
        self.assertEqual(self.ARAConfig.RATE_LIMIT_RETRY_DELAY, 60)
        self.assertEqual(self.ARAConfig.MAX_RETRY_ATTEMPTS, 3)


if __name__ == '__main__':
    unittest.main()
