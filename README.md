# Secure User App – FastAPI + PostgreSQL + Docker + CI/CD

This project implements a **secure user registration API** using FastAPI, SQLAlchemy, and Pydantic.  
It includes password hashing, validation, automated tests, Dockerization, and a CI/CD pipeline that builds and pushes an image to Docker Hub.

---

## Features

# Secure User App – FastAPI + PostgreSQL + Docker + CI/CD

This repository implements a small FastAPI application for secure user registration and also includes a new Calculation model, validation, and thorough tests added in Module 11.

Summary of recent changes

- Added a persistent `Calculation` SQLAlchemy model (fields: `id`, `a`, `b`, `type`, `result`, `created_at`).
- Implemented a calculation factory (`app/calculations.py`) for operations: `Add`, `Sub`, `Multiply`, `Divide`.
- Added Pydantic schemas `CalculationCreate` and `CalculationRead` with validation.
- CRUD helpers to create and fetch calculations in `app/crud.py` (creates and stores computed `result`).
- Added unit and integration tests for calculations and coverage helpers. The test suite reaches 100% coverage for the `app` package.
- Updated CI (`.github/workflows/ci.yml`) to run tests with coverage and to push Docker images on success.

---

## Features

- FastAPI backend with the existing `/users/` endpoint
- SQLAlchemy `User` model (existing)
- New SQLAlchemy `Calculation` model (see above)
- Pydantic schemas for users and calculations
- Calculation factory pattern to encapsulate operation logic
- Password hashing and verification using `passlib`
- Unit and integration tests (`pytest`) with enforced coverage
- Dockerfile + `docker-compose.yml` for running app + PostgreSQL
- GitHub Actions CI: runs tests and pushes Docker image on successful test runs

---

## Tech Stack

- Language: Python
- Framework: FastAPI
- ORM: SQLAlchemy
- Validation: Pydantic
- Auth / Hashing: passlib (pbkdf2_sha256)
- Databases: PostgreSQL (for Docker / CI), SQLite (for local tests)
- Containers: Docker, docker-compose
- CI/CD: GitHub Actions
- Registry: Docker Hub (`pmanu2/secure-user-app`)

---

## Project Structure

```text
secure-user-app/
├── app/
│   ├── main.py          # FastAPI application, routes, dependency injection
│   ├── database.py      # SQLAlchemy engine, SessionLocal, Base
│   ├── models.py        # SQLAlchemy models: User, Calculation
│   ├── schemas.py       # Pydantic schemas (UserCreate, UserRead, CalculationCreate, CalculationRead)
│   ├── crud.py          # CRUD functions for users & calculations
│   ├── calculations.py  # Calculation factory and operation implementations
│   └── security.py      # Password hashing and verification
├── tests/               # Unit + integration tests
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
- **Login:** `POST /users/login` — Authenticate user (username + password; returns user info if valid)
- **Create User:** `POST /users/` — Alias for registration

### Testing All Endpoints

Use the OpenAPI/Swagger UI at `http://localhost:8000/docs` to:
1. Register a new user via `/users/register`
2. Login with `/users/login`
3. Create, read, update, and delete calculations via the `/calculations` endpoints

Or use curl/httpie:

```bash
# Register
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123"}'

# Login
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

Note: Module 12 will add BREAD endpoints for calculations; for now, calculations are exercised via unit/integration tests and the CRUD helpers.

## CI/CD (GitHub Actions)

- Workflow: `.github/workflows/ci.yml`
- On push to `main`, the job:
  - Starts a PostgreSQL service inside the runner
  - Sets `TEST_DATABASE_URL` to point at the service
  - Installs dependencies
  - Runs `pytest` with coverage and fails the job if coverage < 100%
- After tests succeed, the `build-and-push` job builds and pushes an image to Docker Hub using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets.

If Actions fails with DB hostname resolution, the workflow was updated to use `localhost` for `TEST_DATABASE_URL` so the runner connects through the mapped port.

## Docker Hub

The image (when built by CI) is pushed to Docker Hub under the repository `pmanu2/secure-user-app` with the `latest` tag.

Pull with:

```bash
docker pull pmanu2/secure-user-app:latest
```

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
