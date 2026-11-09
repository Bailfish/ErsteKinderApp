"""Pytest fixtures for ErsteKinderApp test suite."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Provide a FastAPI TestClient instance."""
    return TestClient(app)
