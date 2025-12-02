"""
Playwright E2E tests for authentication flows.
Tests both registration and login with positive and negative scenarios.
"""
import pytest
from playwright.sync_api import sync_playwright
import time
import subprocess
import os


@pytest.fixture(scope="session")
def server():
    """Start the FastAPI server for the duration of the test session."""
    # Start the server in background
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///./test_e2e.db"
    
    process = subprocess.Popen(
        [
            "python", "-m", "uvicorn",
            "app.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start by polling the register page
    import urllib.request
    started = False
    timeout_seconds = 30
    start_time = time.time()
    url = "http://127.0.0.1:8000/register.html"
    while time.time() - start_time < timeout_seconds:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    started = True
                    break
        except Exception:
            time.sleep(0.5)

    if not started:
        # Capture server stderr for debugging
        try:
            out, err = process.communicate(timeout=1)
        except Exception:
            process.kill()
            out, err = b"", b""
        raise RuntimeError(f"Server did not start within {timeout_seconds}s. Stderr:\n{err.decode(errors='ignore')}")

    yield process
    
    # Stop the server
    process.terminate()
    process.wait()


@pytest.fixture
def browser():
    """Create a browser instance for each test."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


def test_register_user_success(server, browser):
    """Test successful user registration with valid data."""
    page = browser.new_page()
    
    try:
        page.goto("http://127.0.0.1:8000/register.html")
        
        # Fill in registration form
        page.fill('input[name="username"]', f"testuser_{int(time.time())}")
        page.fill('input[name="email"]', f"test_{int(time.time())}@example.com")
        page.fill('input[name="password"]', "validpassword123")
        page.fill('input[name="confirmPassword"]', "validpassword123")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard (success)
        page.wait_for_url("**/dashboard.html", timeout=5000)
        
        # Verify redirect happened (success)
        assert page.url.endswith("/dashboard.html") or "success" in page.content().lower()
        
    finally:
        page.close()


def test_register_user_invalid_email(server, browser):
    """Test registration with invalid email format."""
    page = browser.new_page()
    
    try:
        page.goto("http://127.0.0.1:8000/register.html")
        
        # Fill in registration form with invalid email
        page.fill('input[name="username"]', f"testuser_{int(time.time())}")
        page.fill('input[name="email"]', "not-an-email")
        page.fill('input[name="password"]', "validpassword123")
        page.fill('input[name="confirmPassword"]', "validpassword123")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for client-side validation error to appear
        page.wait_for_selector('.error-message.show', timeout=2000)
        error_messages = page.query_selector_all('.error-message.show')
        assert len(error_messages) > 0, "Expected validation error to be shown"
        
        # Verify we're still on register page (not submitted)
        assert page.url == "http://127.0.0.1:8000/register.html"
        
    finally:
        page.close()


def test_register_user_short_password(server, browser):
    """Test registration with password that is too short."""
    page = browser.new_page()
    
    try:
        page.goto("http://127.0.0.1:8000/register.html")
        
        # Fill in registration form with short password
        page.fill('input[name="username"]', f"testuser_{int(time.time())}")
        page.fill('input[name="email"]', f"test_{int(time.time())}@example.com")
        page.fill('input[name="password"]', "123")
        page.fill('input[name="confirmPassword"]', "123")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait a bit for client-side validation
        time.sleep(1)
        
        # Check for error message
        error_messages = page.query_selector_all('.error-message.show')
        assert len(error_messages) > 0, "Expected validation error for short password"
        
    finally:
        page.close()


def test_register_user_password_mismatch(server, browser):
    """Test registration with mismatched confirm password."""
    page = browser.new_page()
    
    try:
        page.goto("http://127.0.0.1:8000/register.html")
        
        # Fill in registration form with mismatched passwords
        page.fill('input[name="username"]', f"testuser_{int(time.time())}")
        page.fill('input[name="email"]', f"test_{int(time.time())}@example.com")
        page.fill('input[name="password"]', "password123")
        page.fill('input[name="confirmPassword"]', "password456")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait a bit for client-side validation
        time.sleep(1)
        
        # Check for error message
        error_messages = page.query_selector_all('.error-message.show')
        assert len(error_messages) > 0, "Expected validation error for password mismatch"
        
    finally:
        page.close()


def test_login_user_success(server, browser):
    """Test successful user login with valid credentials."""
    page = browser.new_page()
    
    try:
        # First, register a user
        page.goto("http://127.0.0.1:8000/register.html")
        
        username = f"logintest_{int(time.time())}"
        email = f"logintest_{int(time.time())}@example.com"
        password = "securepassword123"
        
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirmPassword"]', password)
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard after registration
        page.wait_for_url("**/dashboard.html", timeout=5000)
        
        # Now test login on a new page
        page2 = browser.new_page()
        page2.goto("http://127.0.0.1:8000/login.html")
        
        page2.fill('input[name="username"]', username)
        page2.fill('input[name="password"]', password)
        page2.click('button[type="submit"]')
        
        # Wait for redirect
        page2.wait_for_url("**/dashboard.html", timeout=5000)
        
        # Verify we're redirected to dashboard
        assert "dashboard" in page2.url
        
        page2.close()
        
    finally:
        page.close()


def test_login_user_invalid_password(server, browser):
    """Test login with incorrect password."""
    page = browser.new_page()
    
    try:
        # First, register a user
        page.goto("http://127.0.0.1:8000/register.html")
        
        username = f"invalidpwtest_{int(time.time())}"
        email = f"invalidpwtest_{int(time.time())}@example.com"
        password = "correctpassword123"
        
        page.fill('input[name="username"]', username)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.fill('input[name="confirmPassword"]', password)
        page.click('button[type="submit"]')
        
        # Wait for registration to complete
        time.sleep(2)
        
        # Now test login with wrong password
        page2 = browser.new_page()
        page2.goto("http://127.0.0.1:8000/login.html")
        
        page2.fill('input[name="username"]', username)
        page2.fill('input[name="password"]', "wrongpassword123")
        page2.click('button[type="submit"]')
        
        # Wait for error message
        time.sleep(1)
        
        # Check for error message
        server_error = page2.query_selector('.server-error.show')
        assert server_error is not None, "Expected server error message for wrong password"
        
        # Verify we're still on login page
        assert page2.url == "http://127.0.0.1:8000/login.html"
        
        page2.close()
        
    finally:
        page.close()


def test_login_user_nonexistent(server, browser):
    """Test login with non-existent username."""
    page = browser.new_page()
    
    try:
        page.goto("http://127.0.0.1:8000/login.html")
        
        page.fill('input[name="username"]', f"nonexistent_{int(time.time())}")
        page.fill('input[name="password"]', "anypassword123")
        page.click('button[type="submit"]')
        
        # Wait for error message
        time.sleep(1)
        
        # Check for error message
        server_error = page.query_selector('.server-error.show')
        assert server_error is not None, "Expected error message for non-existent user"
        
    finally:
        page.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
