from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_LENGTH = 72  # bcrypt only uses first 72 bytes


def _trim_password(password: str) -> str:
    # Safely trim to 72 characters so bcrypt never raises
    # (tests in CI use very long passwords)
    return password[:MAX_BCRYPT_LENGTH]


def hash_password(password: str) -> str:
    trimmed = _trim_password(password)
    return pwd_context.hash(trimmed)


def verify_password(password: str, hashed: str) -> bool:
    trimmed = _trim_password(password)
    return pwd_context.verify(trimmed, hashed)
