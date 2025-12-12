import time


def test_create_power_via_ui(server, browser):
    base = "http://127.0.0.1:8000"
    page = browser.new_page()

    # register user
    ts = str(int(time.time()))
    username = f"pow_user_{ts}"
    email = f"{username}@example.com"
    password = "secret123"

    page.goto(base + "/register.html")
    page.fill('input#username', username)
    page.fill('input#email', email)
    page.fill('input#password', password)
    page.fill('input#confirmPassword', password)
    page.click('button#submitBtn')
    page.wait_for_url(base + '/dashboard.html', timeout=5000)

    # create a power calculation (2^5 = 32)
    page.fill('#inputA', '2')
    page.fill('#inputB', '5')
    page.select_option('#inputType', 'Power')
    page.click('#createCalc')

    # wait up to 3s for the new row to appear with result 32
    found = False
    deadline = time.time() + 3.0
    while time.time() < deadline:
        page.wait_for_timeout(300)
        rows = page.locator('#calculationsBody tr')
        try:
            count = rows.count()
        except Exception:
            count = 0
        if count and count >= 1:
            for i in range(count):
                text = rows.nth(i).inner_text()
                if '32' in text or '32.0' in text:
                    found = True
                    break
        if found:
            break
    if not found:
        # dump page HTML to help debugging
        print('DEBUG PAGE CONTENT:\n', page.content())
    assert found, 'Created power result not found in table'

    page.close()
