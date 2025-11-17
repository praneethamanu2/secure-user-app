from app.security import verify_password


def test_create_user(client):
    payload = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "secret123",
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "user1"
    assert data["email"] == "user1@example.com"
    assert "id" in data
    assert "created_at" in data


def test_duplicate_username(client):
    user1 = {
        "username": "sameuser",
        "email": "first@example.com",
        "password": "secret123",
    }
    user2 = {
        "username": "sameuser",  # same username, different email
        "email": "second@example.com",
        "password": "secret123",
    }

    r1 = client.post("/users/", json=user1)
    assert r1.status_code == 201

    r2 = client.post("/users/", json=user2)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Username already exists"


def test_duplicate_email(client):
    user1 = {
        "username": "user_a",
        "email": "dupe@example.com",
        "password": "secret123",
    }
    user2 = {
        "username": "user_b",  # different username, same email
        "email": "dupe@example.com",
        "password": "secret123",
    }

    r1 = client.post("/users/", json=user1)
    assert r1.status_code == 201

    r2 = client.post("/users/", json=user2)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already exists"
