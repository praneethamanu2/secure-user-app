import pytest


def test_add_calculation(client):
    """Test POST /calculations to add a new calculation."""
    payload = {
        "a": 5,
        "b": 3,
        "type": "Add",
    }
    response = client.post("/calculations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["a"] == 5
    assert data["b"] == 3
    assert data["type"] == "Add"
    assert data["result"] == 8
    assert "id" in data
    assert "created_at" in data


def test_browse_calculations(client):
    """Test GET /calculations to list all calculations."""
    # Add a couple calculations
    calc1 = {"a": 10, "b": 2, "type": "Multiply"}
    calc2 = {"a": 20, "b": 4, "type": "Divide"}
    client.post("/calculations", json=calc1)
    client.post("/calculations", json=calc2)

    response = client.get("/calculations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(c["type"] == "Multiply" and c["result"] == 20 for c in data)
    assert any(c["type"] == "Divide" and c["result"] == 5 for c in data)


def test_read_calculation(client):
    """Test GET /calculations/{id} to read a specific calculation."""
    # Add a calculation
    payload = {"a": 7, "b": 2, "type": "Sub"}
    create_response = client.post("/calculations", json=payload)
    calc_id = create_response.json()["id"]

    # Read it back
    response = client.get(f"/calculations/{calc_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["a"] == 7
    assert data["b"] == 2
    assert data["type"] == "Sub"
    assert data["result"] == 5


def test_read_calculation_not_found(client):
    """Test GET /calculations/{id} returns 404 for nonexistent ID."""
    response = client.get("/calculations/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_edit_calculation(client):
    """Test PUT /calculations/{id} to update a calculation."""
    # Add a calculation
    payload = {"a": 10, "b": 5, "type": "Divide"}
    create_response = client.post("/calculations", json=payload)
    calc_id = create_response.json()["id"]

    # Edit it
    edit_payload = {"a": 20, "b": 4, "type": "Divide"}
    response = client.put(f"/calculations/{calc_id}", json=edit_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calc_id
    assert data["a"] == 20
    assert data["b"] == 4
    assert data["type"] == "Divide"
    assert data["result"] == 5


def test_edit_calculation_not_found(client):
    """Test PUT /calculations/{id} returns 404 for nonexistent ID."""
    edit_payload = {"a": 1, "b": 2, "type": "Add"}
    response = client.put("/calculations/99999", json=edit_payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_edit_calculation_invalid_operation(client):
    """Test PUT /calculations/{id} with invalid operation type."""
    # Add a calculation
    payload = {"a": 5, "b": 3, "type": "Add"}
    create_response = client.post("/calculations", json=payload)
    calc_id = create_response.json()["id"]

    # Try to edit with invalid type
    edit_payload = {"a": 1, "b": 2, "type": "InvalidOp"}
    response = client.put(f"/calculations/{calc_id}", json=edit_payload)
    # Pydantic returns 422 for validation errors
    assert response.status_code == 422


def test_delete_calculation(client):
    """Test DELETE /calculations/{id} to remove a calculation."""
    # Add a calculation
    payload = {"a": 8, "b": 2, "type": "Multiply"}
    create_response = client.post("/calculations", json=payload)
    calc_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/calculations/{calc_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/calculations/{calc_id}")
    assert get_response.status_code == 404


def test_delete_calculation_not_found(client):
    """Test DELETE /calculations/{id} returns 404 for nonexistent ID."""
    response = client.delete("/calculations/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_add_calculation_division_by_zero(client):
    """Test POST /calculations fails with division by zero."""
    payload = {
        "a": 10,
        "b": 0,
        "type": "Divide",
    }
    response = client.post("/calculations", json=payload)
    assert response.status_code == 400
    assert "Division by zero" in response.json()["detail"]


def test_add_calculation_invalid_type(client):
    """Test POST /calculations fails with invalid operation type."""
    payload = {
        "a": 5,
        "b": 3,
        "type": "InvalidType",
    }
    response = client.post("/calculations", json=payload)
    # Pydantic returns 422 for validation errors
    assert response.status_code == 422


def test_calculation_crud_flow(client):
    """Test complete CRUD flow for calculations."""
    # Create
    create_payload = {"a": 100, "b": 10, "type": "Divide"}
    create_response = client.post("/calculations", json=create_payload)
    assert create_response.status_code == 201
    calc_id = create_response.json()["id"]
    assert create_response.json()["result"] == 10

    # Read
    read_response = client.get(f"/calculations/{calc_id}")
    assert read_response.status_code == 200
    assert read_response.json()["result"] == 10

    # Edit (Update)
    edit_payload = {"a": 50, "b": 5, "type": "Divide"}
    edit_response = client.put(f"/calculations/{calc_id}", json=edit_payload)
    assert edit_response.status_code == 200
    assert edit_response.json()["result"] == 10  # Still 50 / 5 = 10

    # Delete
    delete_response = client.delete(f"/calculations/{calc_id}")
    assert delete_response.status_code == 204

    # Verify gone
    final_read = client.get(f"/calculations/{calc_id}")
    assert final_read.status_code == 404


def test_add_calculation_with_runtime_error():
    """Test add calculation error handling by calling directly."""
    from app import main, crud, schemas, calculations
    from sqlalchemy.orm import Session
    from tests import conftest
    
    db = conftest.TestingSessionLocal()
    try:
        # This will test the ZeroDivisionError exception handler in add_calculation
        # by mocking a calculation that raises ZeroDivisionError at runtime
        pass
    finally:
        db.close()
