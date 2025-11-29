"""
Configuration Tests
===================

Tests for ARA configuration constants and settings.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARA module using test utilities
from test_utils import get_ara
ara = get_ara()


class TestARAConfig(unittest.TestCase):
    """Test ARA configuration."""
    
    def test_config_constants_exist(self):
        """Test that all required configuration constants are defined."""
        config = ara.ARAConfig()
        
        # API settings
        self.assertIsInstance(config.API_REQUEST_TIMEOUT, int)
        self.assertGreater(config.API_REQUEST_TIMEOUT, 0)
    
    def test_config_token_env_vars(self):
        """Test that token environment variables are properly configured."""
        config = ara.ARAConfig()
        
        self.assertIsInstance(config.TOKEN_ENV_VARS, list)
        self.assertGreater(len(config.TOKEN_ENV_VARS), 0)
        self.assertIn('AZURE_ACCESS_TOKEN', config.TOKEN_ENV_VARS)
    
    def test_config_api_endpoints(self):
        """Test that API endpoints are properly configured."""
        config = ara.ARAConfig()
        
        self.assertTrue(config.AZURE_MANAGEMENT_URL.startswith('https://'))
        self.assertTrue(config.GRAPH_API_URL.startswith('https://'))
    
    def test_config_api_versions(self):
        """Test that API versions are properly configured."""
        config = ara.ARAConfig()
        
        self.assertIsInstance(config.AZURE_API_VERSION, str)
        self.assertIsInstance(config.AUTH_API_VERSION, str)
        self.assertIsInstance(config.MGMT_GROUP_API_VERSION, str)
    
    def test_config_cache_settings(self):
        """Test that cache settings are properly configured."""
        config = ara.ARAConfig()
        
        self.assertIsInstance(config.CACHE_SIZE_LIMIT, int)
        self.assertGreater(config.CACHE_SIZE_LIMIT, 0)


if __name__ == '__main__':
    unittest.main()
