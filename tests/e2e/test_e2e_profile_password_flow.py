import time


def test_profile_password_flow(server, browser):
    """E2E: register -> dashboard -> profile -> change password -> login with new password"""
    base = "http://127.0.0.1:8000"
    page = browser.new_page()

    # register
    ts = str(int(time.time()))
    username = f"e2e_user_{ts}"
    email = f"{username}@example.com"
    password = "secret123"

    page.goto(base + "/register.html")
    page.fill('input#username', username)
    page.fill('input#email', email)
    page.fill('input#password', password)
    page.fill('input#confirmPassword', password)
    page.click('button#submitBtn')

    # wait for redirect to dashboard
    page.wait_for_url(base + '/dashboard.html', timeout=5000)

    # open avatar menu and go to profile
    page.click('#avatarImg')
    page.click('#menuProfile')
    page.wait_for_url(base + '/profile.html', timeout=5000)

    # change password
    page.fill('#currentPassword', password)
    page.fill('#newPassword', 'newsecret456')
    page.click('#changePassword')

    # profile page clears token and redirects to login; wait for login page
    page.wait_for_url(base + '/login.html', timeout=5000)

    # login with new password
    page.fill('input#username', username)
    page.fill('input#password', 'newsecret456')
    page.click('button#submitBtn')
    page.wait_for_url(base + '/dashboard.html', timeout=5000)

    # verify we're signed in (username/email visible)
    assert page.locator('#username').inner_text().strip() != ''

    page.close()
