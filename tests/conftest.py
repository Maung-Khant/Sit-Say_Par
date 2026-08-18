# tests/conftest.py
import sys
from pathlib import Path

import pytest

# Add project root to sys.path so that 'backend' can be imported
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import and call init_db to create tables before any tests run
from backend.infrastructure.database import init_db


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init_db()
