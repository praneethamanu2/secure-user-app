"""
Test coverage for static file serving routes.
"""
import pytest
from app.main import get_register, get_login


def test_get_register_route(client):
    """Test GET /register.html endpoint."""
    response = client.get("/register.html")
    assert response.status_code == 200
    # Check that HTML content is returned
    content = response.text
    assert "Register" in content or "Create Account" in content


def test_get_login_route(client):
    """Test GET /login.html endpoint."""
    response = client.get("/login.html")
    assert response.status_code == 200
    # Check that HTML content is returned
    content = response.text
    assert "Login" in content or "login" in content.lower()
