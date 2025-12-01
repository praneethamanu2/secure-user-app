import pytest


def test_register_user(client):
    """Test user registration via POST /users/register."""
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepass123",
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "testuser@example.com"
    assert "id" in data["user"]


def test_register_duplicate_username(client):
    """Test registration fails with duplicate username."""
    payload1 = {
        "username": "duplicate_user",
        "email": "first@example.com",
        "password": "pass123",
    }
    payload2 = {
        "username": "duplicate_user",
        "email": "second@example.com",
        "password": "pass123",
    }
    client.post("/users/register", json=payload1)
    response = client.post("/users/register", json=payload2)
    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]


def test_register_duplicate_email(client):
    """Test registration fails with duplicate email."""
    payload1 = {
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "pass123",
    }
    payload2 = {
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "pass123",
    }
    client.post("/users/register", json=payload1)
    response = client.post("/users/register", json=payload2)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]


def test_login_success(client):
    """Test successful login."""
    # First register a user
    register_payload = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "mypassword123",
    }
    client.post("/users/register", json=register_payload)

    # Then login
    login_payload = {
        "username": "loginuser",
        "password": "mypassword123",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "loginuser"
    assert data["user"]["email"] == "loginuser@example.com"
    assert "id" in data["user"]


def test_login_invalid_password(client):
    """Test login fails with wrong password."""
    # First register a user
    register_payload = {
        "username": "wrongpwuser",
        "email": "wrongpwuser@example.com",
        "password": "correctpassword",
    }
    client.post("/users/register", json=register_payload)

    # Try to login with wrong password
    login_payload = {
        "username": "wrongpwuser",
        "password": "wrongpassword",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login fails with non-existent user."""
    login_payload = {
        "username": "doesnotexist",
        "password": "anypassword",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]
