"""
Unit tests for authentication endpoints and Firebase token verification.
Tests mock Firebase token verification per CLAUDE.md Section 14 (What NOT to test: Firebase SDK calls).
"""

from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_current_user
from app.main import app
from app.schemas.auth import AuthUser


@pytest.fixture()
def mock_current_user():
    """Mock get_current_user to return a test user."""
    async def _mock_get_current_user():
        return AuthUser(
            id=uuid.uuid4(),
            email="test@example.com",
            display_name="Test User",
            is_active=True,
        )
    
    return _mock_get_current_user


@pytest.fixture()
def client_with_auth(mock_current_user):
    """Test client with mocked get_current_user dependency."""
    app.dependency_overrides[get_current_user] = mock_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_current_user_without_token():
    """Test get_current_user() without authorization header returns 401."""
    client = TestClient(app)
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert "Authorization header missing" in response.json()["detail"]


def test_get_current_user_invalid_header_format():
    """Test get_current_user() with invalid Bearer format returns 401."""
    client = TestClient(app)
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "InvalidFormat token-here"}
    )
    assert response.status_code == 401
    assert "Invalid authorization header format" in response.json()["detail"]


def test_get_me_with_valid_user(client_with_auth: TestClient):
    """Test /auth/me endpoint with mocked valid user."""
    response = client_with_auth.get("/api/v1/auth/me")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["display_name"] == "Test User"
    assert data["is_active"] is True

