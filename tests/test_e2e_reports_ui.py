"""
E2E Playwright test: verify dashboard shows stats and recent history
"""
import time
import os


def screenshot_path(name: str) -> str:
    os.makedirs('e2e_screenshots', exist_ok=True)
    ts = int(time.time())
    return os.path.join('e2e_screenshots', f"{ts}_{name}.png")


def register_and_login(page, username, email, password):
    page.goto('http://127.0.0.1:8000/register.html')
    page.fill('input[name="username"]', username)
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.fill('input[name="confirmPassword"]', password)
    page.click('button[type="submit"]')
    page.wait_for_url('**/dashboard.html', timeout=5000)


def test_reports_ui_flow(server, browser):
    page = browser.new_page()
    try:
        username = f"e2e_reports_{int(time.time())}"
        email = f"{username}@example.com"
        password = "testpassword123"

        register_and_login(page, username, email, password)

        # ensure stat elements are present
        page.wait_for_selector('#statTotal')
        page.wait_for_selector('#historyList')

        # create a calculation via UI
        page.fill('input#inputA', '2')
        page.fill('input#inputB', '3')
        page.select_option('select#inputType', 'Add')
        page.click('button#createCalc')
        page.wait_for_timeout(700)

        # stats should show at least 1
        total_text = page.inner_text('#statTotal')
        assert total_text.strip() != '-' and int(total_text) >= 1

        # history should contain at least one item
        hist = page.query_selector_all('#historyList li')
        assert len(hist) >= 1

        # screenshot
        page.screenshot(path=screenshot_path('reports_ui_after_create'))

    finally:
        page.close()
