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
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data


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
    r1 = client.post("/users/register", json=payload1)
    assert r1.status_code == 201

    r2 = client.post("/users/register", json=payload2)
    assert r2.status_code == 400
    assert "Username already exists" in r2.json()["detail"]


def test_register_duplicate_email(client):
    """Test registration fails with duplicate email."""
    payload1 = {
        "username": "user_a",
        "email": "duplicate@example.com",
        "password": "pass123",
    }
    payload2 = {
        "username": "user_b",
        "email": "duplicate@example.com",
        "password": "pass123",
    }
    r1 = client.post("/users/register", json=payload1)
    assert r1.status_code == 201

    r2 = client.post("/users/register", json=payload2)
    assert r2.status_code == 400
    assert "Email already exists" in r2.json()["detail"]


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
    assert data["username"] == "loginuser"
    assert data["email"] == "loginuser@example.com"
    assert "password" not in data


def test_login_invalid_password(client):
    """Test login fails with invalid password."""
    # Register a user
    register_payload = {
        "username": "passuser",
        "email": "passuser@example.com",
        "password": "correctpass",
    }
    client.post("/users/register", json=register_payload)

    # Try login with wrong password
    login_payload = {
        "username": "passuser",
        "password": "wrongpass",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login fails for nonexistent user."""
    login_payload = {
        "username": "nonexistent",
        "password": "anypass",
    }
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]
