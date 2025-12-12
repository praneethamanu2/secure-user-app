"""
E2E Playwright tests for calculation BREAD flows: create, read (list), edit, delete.
Saves screenshots into `e2e_screenshots/` for submission.
"""
import time
import os
import pytest

# Use fixtures `server` and `browser` from tests/test_e2e_playwright.py by name

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
    # wait for redirect to dashboard
    page.wait_for_url('**/dashboard.html', timeout=5000)


@pytest.mark.order(1)
def test_calculation_bread_flow(server, browser):
    page = browser.new_page()
    try:
        username = f"e2e_user_{int(time.time())}"
        email = f"{username}@example.com"
        password = "testpassword123"

        # Register and arrive at dashboard
        register_and_login(page, username, email, password)
        # take screenshot of dashboard initial state
        page.screenshot(path=screenshot_path('dashboard_after_register'))

        # create a calculation via UI
        page.fill('input#inputA', '12')
        page.fill('input#inputB', '8')
        page.select_option('select#inputType', 'Add')
        page.click('button#createCalc')
        # wait a bit for the list to refresh
        page.wait_for_timeout(800)
        page.screenshot(path=screenshot_path('after_create'))

        # find created row (search for result 20)
        content = page.content()
        assert '20' in content

        # Edit the first calculation in the list: click its Edit button
        # We assume table rows render with Edit buttons; click first Edit.
        edit_buttons = page.query_selector_all('button:has-text("Edit")')
        assert len(edit_buttons) > 0
        # determine which row we're editing so we can verify deletion later
        row_el = edit_buttons[0]
        row_id = row_el.evaluate("el => el.closest('tr') && el.closest('tr').id")
        edit_buttons[0].click()
        page.wait_for_timeout(200)
        # change values
        page.fill(f'input[id^="edit-a-"]', '30')
        page.fill(f'input[id^="edit-b-"]', '5')
        # select Divide
        page.select_option('select[id^="edit-type-"]', 'Divide')
        # save
        save_buttons = page.query_selector_all('button:has-text("Save")')
        assert len(save_buttons) > 0
        save_buttons[0].click()
        page.wait_for_timeout(800)
        page.screenshot(path=screenshot_path('after_edit'))

        # verify updated result 6 (30/5) within the edited row
        edited_row = page.query_selector(f'#{row_id}')
        assert edited_row is not None
        assert '6' in edited_row.inner_text()

        # Delete the edited calculation (click corresponding Delete)
        delete_buttons = page.query_selector_all('button:has-text("Delete")')
        assert len(delete_buttons) > 0
        # click first delete and accept confirm
        # register a one-time dialog handler to accept the confirm
        def _on_dialog(d):
            try:
                d.accept()
            except Exception:
                pass

        page.on('dialog', _on_dialog)
        delete_buttons[0].click()
        # give dialog handler time to run
        page.wait_for_timeout(300)
        page.wait_for_timeout(500)
        page.screenshot(path=screenshot_path('after_delete'))

        # verify removed: the edited row should be gone
        assert page.query_selector(f'#{row_id}') is None

    finally:
        page.close()
