#!/usr/bin/env python3
"""
Script to capture screenshots of the Playwright E2E tests.
"""
import subprocess
import os
import time
from pathlib import Path

# Create screenshots directory
screenshots_dir = Path("./e2e_screenshots")
screenshots_dir.mkdir(exist_ok=True)

# Start server
env = os.environ.copy()
env["DATABASE_URL"] = "sqlite:///./test_e2e.db"

print("Starting server...")
process = subprocess.Popen(
    ["python", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server
import urllib.request
started = False
for i in range(30):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/register.html", timeout=1):
            started = True
            break
    except:
        time.sleep(0.5)

if not started:
    print("Server failed to start")
    process.terminate()
    exit(1)

print("Server started! Capturing screenshots...")
time.sleep(1)

# Capture screenshots using Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Screenshot 1: Register page
    print("Capturing register page...")
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000/register.html")
    page.screenshot(path=str(screenshots_dir / "01_register_page.png"))
    page.close()
    
    # Screenshot 2: Login page
    print("Capturing login page...")
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000/login.html")
    page.screenshot(path=str(screenshots_dir / "02_login_page.png"))
    page.close()
    
    # Screenshot 3: Register form filled
    print("Capturing register form with data...")
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000/register.html")
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)
    page.fill('input#username', "testuser123")
    page.fill('input#email', "test@example.com")
    page.fill('input#password', "SecurePass123!")
    page.fill('input#confirmPassword', "SecurePass123!")
    page.screenshot(path=str(screenshots_dir / "03_register_form_filled.png"))
    page.close()
    
    # Screenshot 4: Dashboard after login
    print("Capturing dashboard after successful registration...")
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000/register.html")
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)
    uid = int(time.time())
    page.fill('input#username', f"testuser{uid}")
    page.fill('input#email', f"test{uid}@example.com")
    page.fill('input#password', "SecurePass123!")
    page.fill('input#confirmPassword', "SecurePass123!")
    page.click('button#submitBtn')
    page.wait_for_url("http://127.0.0.1:8000/dashboard.html", timeout=10000)
    time.sleep(1)
    page.screenshot(path=str(screenshots_dir / "04_dashboard_after_registration.png"))
    
    browser.close()

print(f"\n✅ Screenshots saved to {screenshots_dir}/")
print("Files:")
for f in sorted(screenshots_dir.glob("*.png")):
    print(f"  - {f.name}")

# Stop server
process.terminate()
process.wait(timeout=5)
print("✅ Server stopped")
