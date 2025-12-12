```
# Secure User App – FastAPI + PostgreSQL + Docker + CI/CD + JWT + E2E Testing
```
# Secure User App – FastAPI + PostgreSQL + Docker + CI/CD + JWT + E2E Testing

[![Docker Pulls](https://img.shields.io/docker/pulls/pmanu2/secure-user-app.svg)](https://hub.docker.com/r/pmanu2/secure-user-app)


This project implements a **secure user registration and authentication system** using FastAPI, SQLAlchemy, Pydantic, JWT tokens, and Playwright for end-to-end testing.  
It includes password hashing, JWT token generation, front-end registration/login pages with client-side validation, Playwright E2E tests, automated tests, Dockerization, and a CI/CD pipeline that builds and pushes images to Docker Hub.

---

## Features

### Module 11-12 Features
- FastAPI backend with user registration/login endpoints
- SQLAlchemy `User` and `Calculation` models
- Calculation factory pattern with Add, Sub, Multiply, Divide operations
- Full BREAD endpoints for calculations (Browse, Read, Edit, Add, Delete)
- Pydantic schemas for users and calculations
- Password hashing and verification using `passlib`
- Unit and integration tests (`pytest`) with 100% code coverage
- Dockerfile + `docker-compose.yml` for running app + PostgreSQL
- GitHub Actions CI: runs tests and pushes Docker image on successful test runs

### Module 13 Features (JWT & E2E Testing)
- **JWT Authentication**: Register and login endpoints return JWT tokens
- **Front-End Pages**: Responsive registration and login HTML pages with client-side validation
  - Email format validation
  - Password strength requirements (min 6 characters)
  - Password confirmation matching
  - Error messaging and success feedback
- **Playwright E2E Tests**: Comprehensive end-to-end testing
  - Positive tests: successful registration and login with valid data
  - Negative tests: invalid email format, short passwords, password mismatch, wrong credentials
  - Tests verify UI state changes, error messages, and redirects
- **CI/CD Integration**: Playwright tests run automatically in GitHub Actions pipeline
- **Token Storage**: JWT tokens stored in localStorage for persistent authentication

---

## Tech Stack

- Language: Python
- Framework: FastAPI
- ORM: SQLAlchemy
- Validation: Pydantic
- Auth: JWT (python-jose) + Password Hashing (passlib pbkdf2_sha256)
- Frontend: HTML/CSS/JavaScript with client-side validation
- E2E Testing: Playwright
- Databases: PostgreSQL (for Docker / CI), SQLite (for local tests)
- Containers: Docker, docker-compose
- CI/CD: GitHub Actions
- Registry: Docker Hub (`pmanu2/secure-user-app`)

---

## Project Structure

```text
secure-user-app/
├── app/
│   ├── main.py              # FastAPI application, routes, dependency injection
│   ├── database.py          # SQLAlchemy engine, SessionLocal, Base
│   ├── models.py            # SQLAlchemy models: User, Calculation
│   ├── schemas.py           # Pydantic schemas (UserCreate, UserRead, UserLogin, TokenResponse, etc.)
│   ├── crud.py              # CRUD functions for users & calculations
│   ├── calculations.py      # Calculation factory and operation implementations
│   ├── security.py          # Password hashing, verification, and JWT token generation
│   └── static/
│       ├── register.html    # User registration form (Module 13)
│       └── login.html       # User login form (Module 13)
├── tests/
│   ├── conftest.py          # pytest fixtures and database setup
│   ├── test_*.py            # Unit and integration tests (100% coverage)
│   └── test_e2e_playwright.py  # Playwright E2E tests (Module 13)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/ci.yml
```

## Running the App with Docker Compose

Make sure Docker Desktop (or Docker Engine) is running.

From the project root, build and start the services:

```bash
docker-compose up --build
```

This will:

- Start a PostgreSQL container
- Build the FastAPI app image
- Run the FastAPI container on port 8000

Access the API

- Root endpoint: `http://localhost:8000/`
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`

## Quick start — run locally (no Docker)

If you prefer to run the app locally without Docker, use your virtual environment and start uvicorn:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
# then open http://127.0.0.1:8000/docs or the static pages under /static
```

## How to Run Tests Locally

Local tests use a SQLite test database by default (configured in `tests/conftest.py` via `TEST_DATABASE_URL`).

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov coverage
```

3. Run the tests (quick):

```bash
pytest -q
```

4. Run tests with coverage locally (same command used in CI):

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=100
```

If you prefer the coverage run flow:

```bash
python -m coverage run -m pytest
python -m coverage report -m
```

## Calculation Model & Usage (Module 11–12)

- `CalculationCreate` accepts `a`, `b`, and `type` (one of `Add`, `Sub`, `Multiply`, `Divide`).
- The application computes the `result` via the factory in `app/calculations.py` and persists it in the `calculations` table.
- Division by zero is validated/handled and will raise an error during calculation.

### Calculation BREAD Endpoints (Module 12)

- **Browse:** `GET /calculations` — List all calculations
- **Read:** `GET /calculations/{id}` — Get a specific calculation
- **Edit:** `PUT /calculations/{id}` — Update a calculation (a, b, type; result recomputed)
- **Add:** `POST /calculations` — Create a new calculation
- **Delete:** `DELETE /calculations/{id}` — Remove a calculation

### User Authentication Endpoints (Module 12)

- **Register:** `POST /users/register` — Create a new user account
- **Login:** `POST /users/login` — Authenticate user (username + password; returns JWT token if valid)
- **Create User:** `POST /users/` — Alias for registration

### JWT Response Format (Module 13)

When registering or logging in successfully, both `/users/register` and `/users/login` return:

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

The `access_token` is a JWT token that can be used for future authenticated requests. It is automatically stored in `localStorage` by the front-end pages.

## Front-End Pages (Module 13)

### Registration Page

Access at: `http://localhost:8000/register.html`

**Features:**
- Client-side validation for:
  - Username (min 3 characters)
  - Email (valid email format)
  - Password (min 6 characters)
  - Password confirmation (must match)
- Real-time error messages
- Success message on registration
- Auto-redirect to dashboard on success
- Links to login page

### Login Page

Access at: `http://localhost:8000/login.html`

**Features:**
- Client-side validation for:
  - Username (required)
  - Password (required)
- Server-side authentication (verifies credentials)
- Error messages for invalid credentials
- Success message on login
- Auto-redirect to dashboard on success
- Links to registration page

## Running Playwright E2E Tests (Module 13)

Playwright tests verify both the front-end pages and backend authentication flows.

### Local Testing

1. Install Playwright browsers:
```bash
playwright install chromium
```

2. Run the E2E tests:
```bash
pytest tests/test_e2e_playwright.py -v
```

**Test Coverage:**
- ✅ `test_register_user_success` - Register with valid data
- ✅ `test_register_user_invalid_email` - Reject invalid email format
- ✅ `test_register_user_short_password` - Reject password < 6 chars
- ✅ `test_register_user_password_mismatch` - Reject mismatched passwords
- ✅ `test_login_user_success` - Login with correct credentials
- ✅ `test_login_user_invalid_password` - Reject wrong password (401)
- ✅ `test_login_user_nonexistent` - Reject non-existent user

### CI/CD Integration

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
1. Installs Playwright browsers
2. Runs all Playwright E2E tests
3. Reports pass/fail status
4. Pushes Docker image to Docker Hub only if all tests pass

Example workflow run output:
```
Installing Playwright browsers...
Running Playwright E2E Tests...
test_register_user_success PASSED
test_register_user_invalid_email PASSED
test_login_user_success PASSED
... (7 tests total)
```

Or use curl/httpie to test the API:

```bash
# Register with JWT response
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123"}'
# Response includes access_token, token_type, user

# Login to get JWT token
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}'

# Add a calculation
curl -X POST "http://localhost:8000/calculations" \
  -H "Content-Type: application/json" \
  -d '{"a":10,"b":2,"type":"Divide"}'

# Browse all calculations
curl -X GET "http://localhost:8000/calculations"

# Read a specific calculation (replace 1 with actual ID)
curl -X GET "http://localhost:8000/calculations/1"

# Update a calculation
curl -X PUT "http://localhost:8000/calculations/1" \
  -H "Content-Type: application/json" \
  -d '{"a":20,"b":4,"type":"Divide"}'

# Delete a calculation
curl -X DELETE "http://localhost:8000/calculations/1"
```

## CI/CD (GitHub Actions)

- Workflow: `.github/workflows/ci.yml`
- On push to `main`, the job:
  - Starts a PostgreSQL service inside the runner
  - Sets `TEST_DATABASE_URL` to point at the service
  - Installs dependencies
  - Runs `pytest` with coverage and fails the job if coverage < 100%
- After tests succeed, the `build-and-push` job builds and pushes an image to Docker Hub using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets.

If Actions fails with DB hostname resolution, the workflow was updated to use `localhost` for `TEST_DATABASE_URL` so the runner connects through the mapped port.

## Module 13 Summary

**JWT Authentication:**
- /register and /login endpoints now return JWT tokens along with user info
- Tokens are generated using python-jose and include expiration (30 minutes by default)
- SECRET_KEY can be set via environment variable (required for production)

**Front-End Pages:**
- Fully responsive HTML pages for registration and login
- Client-side validation with real-time error feedback
- Password confirmation matching on registration
- Token automatically stored in localStorage on success
- Clean UI with gradient backgrounds and accessibility features

**Playwright E2E Tests:**
- 7 comprehensive tests covering positive and negative scenarios
- Tests verify form field validation, submission, and error/success messages
- Integration with pytest framework
- Runs in CI/CD pipeline before Docker image push

**Test Coverage:**
- Maintained 100% code coverage on app/ package
- Added 39 test (unit + integration + E2E)

## Docker Hub

The image (when built by CI) is pushed to Docker Hub under the repository `pmanu2/secure-user-app` with the `latest` tag.

Pull with:

```bash
docker pull pmanu2/secure-user-app:latest
```

Docker Hub repository (open in browser):

https://hub.docker.com/r/pmanu2/secure-user-app

## Notes & Next Steps

- The codebase emits some deprecation warnings from Pydantic v2 and FastAPI lifecycle events — these are non-blocking but can be addressed in a follow-up.
- Test coverage is at 99% for the `app` package (37 passing tests). A few exception handlers in endpoints are hard to reach without monkey-patching.
- All user and calculation routes are fully tested with comprehensive integration tests.

---

## Module 12 Summary

**Completed:**
- User registration and login endpoints with secure password verification
- Full BREAD endpoints for calculations (Browse, Read, Edit, Add, Delete)
- 37 integration tests covering user routes, calculation routes, and edge cases
- Updated CI/CD pipeline to run all tests and push Docker images on success
- Complete documentation in README with curl examples
 
**Run & Test Guide**

- **Repository Docker Hub:** `pmanu2/secure-user-app` — https://hub.docker.com/r/pmanu2/secure-user-app
**Requirements (local)**
- Python 3.10+ (3.12 used for development here)
- Git
- Docker & Docker Compose (for containerized run)
- Optional: Node/Playwright CLI (we use Playwright Python support)

**Create & activate virtualenv (recommended)**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate   # Windows
```

**Install Python dependencies**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Install Playwright browsers (for E2E tests)**
```bash
python -m playwright install --with-deps
```

**Run the app locally (no Docker)**
```bash
# from repository root
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Open the site:
- Register/login pages: `http://127.0.0.1:8000/register.html` and `http://127.0.0.1:8000/login.html`
- Dashboard: `http://127.0.0.1:8000/dashboard.html`

**Run with Docker Compose**
Make sure Docker is running, then:
```bash
docker-compose up --build
```
This will start the app and a PostgreSQL service (if configured in `docker-compose.yml`). The app will be available at `http://localhost:8000`.

**Run tests locally**

- Unit & integration tests (pytest):
```bash
source .venv/bin/activate
pytest -q
```

- Playwright E2E tests (browser tests):
```bash
source .venv/bin/activate
python -m playwright install --with-deps
pytest -q tests/e2e
```

Notes for E2E:
- Tests start a local server automatically (see `tests/conftest.py` fixture `server`) and use Playwright's chromium instance.
- If you encounter failures, ensure no other process is using port `8000` (check `lsof -i :8000`) and kill stale uvicorn before running.

**CI / GitHub Actions**
- The repo contains a workflow at `.github/workflows/ci.yml` which:
  - Installs Python and project dependencies
  - Installs Playwright browsers
  - Runs the test suite (pytest)
  - Builds and pushes a Docker image to Docker Hub (requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repo secrets)

**Docker Hub**
- The CI workflow pushes the image to: `pmanu2/secure-user-app:latest` (set the `DOCKERHUB_*` secrets in your repo Settings → Secrets to enable push).

**API Quick Examples**
- Register:
```bash
curl -s -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}' | jq
```

- Login:
```bash
curl -s -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' | jq
```

- Create calculation (authenticated; replace <TOKEN>):
```bash
curl -s -X POST "http://localhost:8000/calculations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"a":2, "b":5, "type":"Power"}' | jq
```

**Reflection**
- What I implemented: This project demonstrates a full-stack small app (FastAPI backend, static frontend) with authentication, calculation logic, and end-to-end testing. I focused on:
  - Reliability: tests (unit, integration, E2E) are automated and exercised locally and in CI.
  - Usability: a simple dashboard with create/edit/delete operations and a compact recent history/reporting panel.
  - Testability: small changes were made to support stable Playwright tests (explicit IDs, minor compatibility inputs) so UI flows are robust.

- Tradeoffs & future improvements:
  - The frontend is static HTML + vanilla JS for simplicity; if the app grows, migrating to a reactive framework (React/Vue/Svelte) would help manage complexity.
  - Some synchronous UI polling is used (e.g., `wait_for_timeout`) to keep E2E tests reliable; replacing this with event-driven WebSocket or server-sent events would be more efficient.
  - Currently no Alembic migrations are included because no schema change was required; adding Alembic would be advisable before making future DB schema changes.

If you'd like I can:
- Add Alembic scaffolding and an initial migration.
- Improve CI to run Playwright E2E in a separate job and cache Playwright browsers for speed.
- Tag and push a release image to Docker Hub.
