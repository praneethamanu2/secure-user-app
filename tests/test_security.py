from app.security import hash_password, verify_password

def test_password_hashing():
    pw = "secret123"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)
