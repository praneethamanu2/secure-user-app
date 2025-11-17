import pytest
from pydantic import ValidationError
from app.schemas import UserCreate

def test_valid_schema():
    obj = UserCreate(username="bob", email="bob@example.com", password="pass123")
    assert obj.username == "bob"

def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="bob", email="bad-email", password="123")
