"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def seed() -> int:
    """Fixed seed for reproducible tests."""
    return 42
