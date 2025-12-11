"""
E2E Playwright test: verify the dashboard stats panel updates
after creating calculations via the UI.
"""
import time
import os
import re


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


def test_stats_flow(server, browser):
    page = browser.new_page()
    try:
        username = f"e2e_stats_{int(time.time())}"
        email = f"{username}@example.com"
        password = "testpassword123"

        register_and_login(page, username, email, password)

        # ensure stats panel is present
        page.wait_for_selector('#statsContent')

        # create two calculations via UI
        page.fill('input#inputA', '2')
        page.fill('input#inputB', '3')
        page.select_option('select#inputType', 'Multiply')
        page.click('button#createCalc')
        page.wait_for_timeout(500)

        page.fill('input#inputA', '10')
        page.fill('input#inputB', '5')
        page.select_option('select#inputType', 'Divide')
        page.click('button#createCalc')
        page.wait_for_timeout(800)

        # check stats content
        content = page.inner_text('#statsContent')
        # Expect something like: "Total: 2 · Avg A: 6 · ..."
        m = re.search(r'Total:\s*(\d+)', content)
        assert m, f"Stats content did not include Total: {content}"
        total = int(m.group(1))
        assert total >= 2

        # save screenshot for submission
        page.screenshot(path=screenshot_path('stats_after_create'))

    finally:
        page.close()
