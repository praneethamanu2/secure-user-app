"""
Additional tests to reach 100% coverage on new JWT code.
"""
import pytest
from app.security import create_access_token
from datetime import timedelta


def test_create_access_token_with_expiration():
    """Test JWT token creation with custom expiration."""
    token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(hours=1)
    )
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    # JWT tokens have 3 parts separated by dots
    assert token.count(".") == 2


def test_create_access_token_default_expiration():
    """Test JWT token creation with default expiration."""
    token = create_access_token(data={"sub": "testuser"})
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    assert token.count(".") == 2
