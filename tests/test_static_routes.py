"""
Test coverage for static file serving routes.
"""
import pytest
from app.main import get_register, get_login, get_dashboard


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


def test_get_dashboard_route(client):
    """Test GET /dashboard.html endpoint."""
    response = client.get("/dashboard.html")
    assert response.status_code == 200
    content = response.text
    assert "Dashboard" in content or "dashboard" in content.lower()


def test_get_dashboard_direct_call():
    """Call the `get_dashboard` function directly to exercise its code paths."""
    resp = get_dashboard()
    # Should return a FileResponse object (Starlette response)
    from starlette.responses import FileResponse
    assert isinstance(resp, FileResponse)
