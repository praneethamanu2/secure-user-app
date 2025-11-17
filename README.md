# Secure User App – FastAPI + PostgreSQL + Docker + CI/CD

This project implements a **secure user registration API** using FastAPI, SQLAlchemy, and Pydantic.  
It includes password hashing, validation, automated tests, Dockerization, and a CI/CD pipeline that builds and pushes an image to Docker Hub.

---

## Features

- FastAPI backend with a `/users/` endpoint
- SQLAlchemy `User` model with:
  - `id`, `username`, `email`, `password_hash`, `created_at`
  - Unique constraints on `username` and `email`
- Pydantic schemas:
  - `UserCreate` for input (username, email, password)
  - `UserRead` for safe output (no password)
- Password hashing and verification using **pbkdf2_sha256** (via passlib)
- Unit and integration tests with `pytest`
- Dockerfile + `docker-compose.yml` for running app + PostgreSQL
- GitHub Actions CI:
  - Runs tests on every push
  - Builds and pushes Docker image to Docker Hub when tests pass

---

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Auth / Hashing:** passlib (pbkdf2_sha256)
- **Databases:** PostgreSQL (for Docker / CI), SQLite (for local tests)
- **Containers:** Docker, docker-compose
- **CI/CD:** GitHub Actions
- **Registry:** Docker Hub (`pmanu2/secure-user-app`)

---

## Project Structure

```text
secure-user-app/
├── app/
│   ├── main.py          # FastAPI application, routes, dependency injection
│   ├── database.py      # SQLAlchemy engine, SessionLocal, Base
│   ├── models.py        # SQLAlchemy User model
│   ├── schemas.py       # Pydantic schemas (UserCreate, UserRead)
│   ├── crud.py          # CRUD functions for users
│   └── security.py      # Password hashing and verification
├── tests/
│   ├── conftest.py              # Test DB setup and TestClient fixture
│   ├── test_schemas.py          # Pydantic validation tests
│   ├── test_security.py         # Password hashing tests
│   └── test_users_integration.py# Integration tests for /users endpoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml       # GitHub Actions CI/CD workflow
**Run the App with Docker Compose**

Make sure Docker Desktop is running.

From the project root, build and start the services:

bash
Copy code
docker-compose up --build
This will:

Start a PostgreSQL container

Build the FastAPI app image

Run the FastAPI container on port 8000

Access the API
Root endpoint:
http://localhost:8000/

Interactive API docs (Swagger UI):
http://localhost:8000/docs

**How to Run Tests Locally** 
To run all unit and integration tests on your local machine:

(Optional) Create and activate a virtual environment:

bash
Copy code
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
pip install pytest
Run the tests:

bash
Copy code
pytest
Locally, tests use a SQLite test database via TEST_DATABASE_URL in tests/conftest.py, so no PostgreSQL container is required for testing.

In CI (GitHub Actions), tests run against a PostgreSQL service.

**Security & Validation**

SQLAlchemy User Model
The User model includes:

id – primary key

username – unique, required

email – unique, required

password_hash – hashed password, never returned to the client

created_at – timestamp

Pydantic Schemas
UserCreate: for incoming data when creating users

Fields: username, email, password

Includes basic validation such as minimum length and valid email format.

UserRead: for outgoing responses

Fields: id, username, email, created_at

Does not expose password_hash.

Password Hashing
app/security.py uses passlib with the pbkdf2_sha256 scheme:

hash_password(password: str) -> str

verify_password(password: str, hashed: str) -> bool

Raw passwords are never stored; only the hashed value is saved in the database.

**API Overview**

POST /users/ – Create User
Request body (UserCreate):

json
Copy code
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "strongpassword123"
}
Successful response (UserRead, HTTP 201):

json
Copy code
{
  "id": 1,
  "username": "exampleuser",
  "email": "user@example.com",
  "created_at": "2025-11-17T15:30:00"
}
Error cases:

Duplicate username → HTTP 400, "Username already exists"

Duplicate email → HTTP 400, "Email already exists"

Invalid email / too-short password → HTTP 422 (validation error)

**CI/CD with GitHub Actions**
The workflow is defined in .github/workflows/ci.yml.

On every push to main:

test job

Starts a PostgreSQL service inside GitHub Actions.

Sets TEST_DATABASE_URL environment variable.

Installs dependencies from requirements.txt.

Runs pytest (unit + integration tests).

build-and-push job (runs only if test succeeds)

Logs into Docker Hub using repository secrets:

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

Builds the Docker image using the Dockerfile.

Pushes the image to Docker Hub as pmanu2/secure-user-app:latest.

You can see workflow runs under the Actions tab in the GitHub repository.

**Docker Hub Repository**
The built image is available publicly on Docker Hub:

Docker Hub repository: https://hub.docker.com/r/pmanu2/secure-user-app

Default tag: latest

Pull it with:

bash
Copy code
docker pull pmanu2/secure-user-app:latest
**Notes**
Local tests use SQLite by default; CI and Docker use PostgreSQL.

Deprecation warnings from Pydantic, Passlib, and FastAPI are known and do not affect functionality for this assignment.

This project is designed as a building block for future modules and can be extended with authentication, additional endpoints, or front-end integration.
