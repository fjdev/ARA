"""
Authentication System Tests
============================

Tests for authentication providers and authentication manager.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARA module using test utilities
from test_utils import get_ara
ara = get_ara()


class TestAuthenticationProviders(unittest.TestCase):
    """Test authentication provider implementations."""
    
    def test_environment_auth_provider_success(self):
        """Test environment auth provider with valid token."""
        test_token = "test_token_123"
        with patch.dict(os.environ, {'AZURE_ACCESS_TOKEN': test_token}):
            provider = ara.EnvironmentAuthProvider()
            self.assertEqual(provider.get_token(), test_token)
    
    def test_environment_auth_provider_no_token(self):
        """Test environment auth provider when no token is available."""
        with patch.dict(os.environ, {}, clear=True):
            provider = ara.EnvironmentAuthProvider()
            self.assertIsNone(provider.get_token())
    
    def test_azure_cli_provider_success(self):
        """Test Azure CLI provider when az command succeeds."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"accessToken": "cli_token_456"}'
        
        with patch('subprocess.run', return_value=mock_result):
            provider = ara.AzureCliAuthProvider()
            self.assertEqual(provider.get_token(), "cli_token_456")
    
    def test_azure_cli_provider_failure(self):
        """Test Azure CLI provider when az command fails."""
        with patch('subprocess.run', side_effect=Exception("az not found")):
            provider = ara.AzureCliAuthProvider()
            self.assertIsNone(provider.get_token())


class TestAuthenticationManager(unittest.TestCase):
    """Test authentication manager."""
    
    def test_authentication_manager_with_env_token(self):
        """Test authentication manager uses environment token when available."""
        test_token = "env_test_token"
        with patch.dict(os.environ, {'AZURE_ACCESS_TOKEN': test_token}):
            with patch.object(ara.AzureAuthenticationManager, '_validate_token', return_value=True):
                manager = ara.AzureAuthenticationManager(allow_interactive=False)
                result = manager.get_token()
                self.assertEqual(result, test_token)
    
    def test_authentication_manager_fallback(self):
        """Test that authentication manager tries providers in order."""
        manager = ara.AzureAuthenticationManager(allow_interactive=False)
        
        # Should try providers and fail gracefully when none work
        with patch.dict(os.environ, {}, clear=True):
            with patch('subprocess.run', side_effect=Exception("az not found")):
                with self.assertRaises(ara.AuthenticationError):
                    manager.get_token()


if __name__ == '__main__':
    unittest.main()
