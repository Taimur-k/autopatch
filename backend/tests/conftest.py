"""
pytest configuration: add the backend directory to sys.path so
that `import app.*` works from the tests/ subdirectory.
"""

import sys
import os

# Insert backend/ (parent of this conftest.py) onto the path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

