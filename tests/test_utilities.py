"""
Utility Functions and Exceptions Tests
======================================

Tests for utility functions and custom exceptions.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ARA module using test utilities
from test_utils import get_ara
ara = get_ara()


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_safe_print_exists(self):
        """Test that safe_print function exists."""
        # Should not raise an exception
        ara.safe_print("Test")
    
    def test_version_defined(self):
        """Test that version is defined."""
        self.assertTrue(hasattr(ara, '__version__'))
        self.assertIsInstance(ara.__version__, str)
        self.assertEqual(ara.__version__, '2.0.0')
    
    def test_author_defined(self):
        """Test that author is defined."""
        self.assertTrue(hasattr(ara, '__author__'))
        self.assertIsInstance(ara.__author__, str)
        self.assertEqual(ara.__author__, 'fjdev')


class TestCustomExceptions(unittest.TestCase):
    """Test custom exception hierarchy."""
    
    def test_ara_error_base(self):
        """Test ARAError base exception."""
        error = ara.ARAError("Test error")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error")
    
    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        error = ara.AuthenticationError("Auth failed")
        self.assertIsInstance(error, ara.ARAError)
        self.assertEqual(str(error), "Auth failed")
    
    def test_api_error(self):
        """Test APIError exception."""
        error = ara.APIError("API failed")
        self.assertIsInstance(error, ara.ARAError)
        self.assertEqual(str(error), "API failed")
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        error = ara.ValidationError("Validation failed")
        self.assertIsInstance(error, ara.ARAError)
        self.assertEqual(str(error), "Validation failed")


if __name__ == '__main__':
    unittest.main()
