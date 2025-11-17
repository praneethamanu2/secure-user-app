import sys
import os

# --- make "app" importable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db

# --- use TEST_DATABASE_URL if set, otherwise fall back to local SQLite ---
TEST_DB = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

connect_args = {}
if TEST_DB.startswith("sqlite"):
    # needed for SQLite in some contexts
    connect_args = {"check_same_thread": False}

engine = create_engine(TEST_DB, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create/drop all tables once per test session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Override FastAPI's get_db dependency to use the test DB."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tell FastAPI to use our override in tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """Return a TestClient for API tests."""
    return TestClient(app)
