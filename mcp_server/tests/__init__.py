"""
Test suite for UOR Evolution MCP Server.
"""

import pytest
import asyncio
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Test configuration
pytest_plugins = ["pytest_asyncio"]

# Common test fixtures and utilities
@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Test constants
TEST_TIMEOUT = 30
TEST_MAX_CONCURRENT = 5
TEST_CONSCIOUSNESS_LEVEL = 0.8
TEST_VM_INSTRUCTIONS = 100
TEST_COSMIC_SCALE = 1e12
