"""
ARA Test Import Utilities
==========================

Utilities for importing the ARA module in tests.
"""

import sys
import os


def import_ara():
    """Import the ARA module from the executable script."""
    # Get the path to the ara script
    ara_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ara")
    
    # Verify the file exists
    if not os.path.exists(ara_path):
        raise ImportError(f"ARA script not found at {ara_path}")
    
    # Read the script content
    with open(ara_path, 'r') as f:
        ara_code = f.read()
    
    # Create a module namespace
    ara_module = type(sys)('ara_module')
    ara_module.__file__ = ara_path
    
    # Add the module to sys.modules to handle imports within the module
    sys.modules["ara_module"] = ara_module
    
    # Execute the module code in the module namespace
    # We'll override __name__ to prevent the main() function from running
    ara_module.__name__ = 'ara_module'
    exec(ara_code, ara_module.__dict__)
    
    return ara_module


# Cache the imported module to avoid repeated imports
_ara_module = None


def get_ara():
    """Get the cached ARA module or import it if not cached."""
    global _ara_module
    if _ara_module is None:
        _ara_module = import_ara()
    return _ara_module
