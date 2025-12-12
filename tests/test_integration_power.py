def test_create_power_calculation(client):
    # register and get token
    res = client.post("/users/register", json={"username": "pow_user", "email": "pow@example.com", "password": "secret123"})
    assert res.status_code == 201
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # create a power calculation 2^8 = 256
    res2 = client.post("/calculations", headers=headers, json={"a": 2, "b": 8, "type": "Power"})
    assert res2.status_code == 201
    data = res2.json()
    assert data["result"] == 256
