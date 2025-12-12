import json


def register_and_token(client, username, email, password):
    res = client.post("/users/register", json={"username": username, "email": email, "password": password})
    assert res.status_code == 201
    data = res.json()
    return data["access_token"], data["user"]


def test_profile_update_persists(client):
    token, user = register_and_token(client, "integ_user", "integ@example.com", "secret123")
    headers = {"Authorization": f"Bearer {token}"}

    # fetch current profile
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "integ_user"

    # update profile
    update = {"username": "integ_user2", "email": "integ2@example.com"}
    r2 = client.put("/users/me", headers=headers, json=update)
    assert r2.status_code == 200
    j = r2.json()
    assert j["username"] == "integ_user2"
    assert j["email"] == "integ2@example.com"

    # fetch again
    r3 = client.get("/users/me", headers=headers)
    assert r3.status_code == 200
    assert r3.json()["username"] == "integ_user2"
