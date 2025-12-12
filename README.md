 
# Secure User App — FastAPI, Docker, JWT, and E2E Testing

[![Docker Pulls](https://img.shields.io/docker/pulls/pmanu2/secure-user-app.svg)](https://hub.docker.com/r/pmanu2/secure-user-app)

This repository provides a small web application demonstrating secure user registration and authentication using FastAPI, SQLAlchemy, Pydantic, and JWT. It includes a static frontend for registration and login, calculation endpoints, automated tests (unit and integration), Playwright end-to-end tests, and a CI workflow for running tests and publishing a Docker image.

---

## Features

- Secure user registration and authentication with JWT tokens
- Password hashing and verification using `passlib`
- Calculation endpoints supporting Add, Sub, Multiply, Divide, and Power operations
- Full BREAD (Browse, Read, Edit, Add, Delete) for calculations
- Static HTML frontend pages for registration, login, dashboard, and profile
- Automated tests: unit, integration, and Playwright E2E tests
- Dockerfile and `docker-compose.yml` for containerized runs
- GitHub Actions workflow to run tests and optionally build/push a Docker image

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Playwright (for E2E tests)
- Docker & Docker Compose
- GitHub Actions (CI)

---

## Project Layout

Key files and folders:

```
app/
  main.py          # FastAPI application and routes
  database.py      # SQLAlchemy engine and session
  models.py        # ORM models for users and calculations
  schemas.py       # Pydantic schemas
  crud.py          # CRUD helpers
  calculations.py  # Calculation operations (Add, Sub, Multiply, Divide, Power)
  security.py      # Password hashing and JWT utilities
  static/          # Frontend HTML/CSS/JS
tests/             # pytest unit/integration and Playwright E2E tests
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
README.md
```

---

## Running Locally (with Docker Compose)

Ensure Docker is running, then from the project root:

```bash
docker-compose up --build
```

This starts a PostgreSQL service and the FastAPI app. The app will be available on port 8000.

- Root: `http://localhost:8000/`
- API docs (Swagger UI): `http://localhost:8000/docs`

## Running Locally (without Docker)

Using a virtual environment is recommended:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for API docs or the static pages under `/static`.

---

## Tests

Local tests use a SQLite test database by default (configured in `tests/conftest.py`).

Install test dependencies and run pytest:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -q
```

To run Playwright E2E tests locally:

```bash
python -m playwright install chromium
pytest tests/test_e2e_playwright.py -v
```

---

## API Overview

Authentication endpoints:

- `POST /users/register` — Create a new user (returns access token)
- `POST /users/login` — Authenticate and receive an access token

Calculation endpoints:

- `GET /calculations` — List calculations
- `GET /calculations/{id}` — Read a calculation
- `POST /calculations` — Create a calculation (body: `a`, `b`, `type`)
- `PUT /calculations/{id}` — Update a calculation
- `DELETE /calculations/{id}` — Delete a calculation

When registration or login succeed, the API returns a JSON object containing an `access_token` and `user` information. The `access_token` is a JWT suitable for Authorization headers.

---

## Playwright E2E Tests and CI

Playwright tests exercise both frontend and backend flows. The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) configured to install dependencies, run tests, and build/push the Docker image when credentials are provided via secrets.

To run E2E tests locally, install Playwright browsers and run the specific test file as shown in the Tests section above.

---

## Docker Hub

An image can be published to Docker Hub under `pmanu2/secure-user-app`. The CI workflow will attempt to push an image if `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set in the repository.

Pull with:

```bash
docker pull pmanu2/secure-user-app:latest
```

More details and examples for using the API are included in this README and the `app/static` frontend pages.

---

## Notes and Next Steps

- The codebase produces some runtime warnings from dependencies; these are non-blocking and can be addressed later.
- If you want database schema migrations, we can add Alembic scaffolding in a follow-up.
- CI can be refined to separate unit/integration and E2E jobs for faster feedback.

---

If you'd like the README reorganized further, shortened, or expanded with examples (curl, httpie, or Postman collections), tell me which sections to change.


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
