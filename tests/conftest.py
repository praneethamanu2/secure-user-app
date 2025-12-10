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

import subprocess
import time
import os
from playwright.sync_api import sync_playwright
import urllib.request

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
    # Clean up database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Clean up after test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def server():
    """Start the FastAPI server for E2E tests for the duration of the test session."""
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///./test_e2e.db"

    process = subprocess.Popen(
        [
            "python", "-m", "uvicorn",
            "app.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to be ready by polling the register page
    started = False
    timeout_seconds = 30
    start_time = time.time()
    url = "http://127.0.0.1:8000/register.html"
    while time.time() - start_time < timeout_seconds:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    started = True
                    break
        except Exception:
            time.sleep(0.5)

    if not started:
        try:
            out, err = process.communicate(timeout=1)
        except Exception:
            process.kill()
            out, err = b"", b""
        raise RuntimeError(f"Server did not start within {timeout_seconds}s. Stderr:\n{err.decode(errors='ignore')}")

    yield process

    process.terminate()
    process.wait()


@pytest.fixture
def browser():
    """Create a Playwright browser instance for each test."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()
