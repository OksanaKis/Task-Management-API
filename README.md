Task Management API

Backend-first REST API for managing tasks, built with FastAPI and PostgreSQL.

This project is developed incrementally as a multi-day backend-focused exercise.
Each day introduces new architectural concepts and production-ready features.

Tech Stack

FastAPI

PostgreSQL

SQLAlchemy 2.0

Alembic (database migrations)

Docker / docker-compose

Pydantic

JWT (OAuth2 Password Flow)

pytest

Project Structure (Current)

app/
  main.py
  init.py
  core/
    config.py
    security.py
  db/
    session.py
    base.py
    base_models.py
    deps.py
  models/
    user.py
    task.py
  schemas/
    user.py
    task.py
    auth_schemas.py
  router/
    auth.py
    tasks.py
    deps_auth.py

tests/
  conftest.py
  test_auth.py
  test_tasks.py

alembic/
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
.env

Day 1 — Core API & Database Setup
Features

Task CRUD endpoints

Request & response validation with Pydantic

PostgreSQL integration

SQLAlchemy 2.0 ORM models

Alembic migrations

Swagger UI (/docs)

Fully Dockerized local environment

Example Endpoints (Day 1)

POST /tasks — create task

GET /tasks — list tasks

GET /tasks/{id} — get task by id

PATCH /tasks/{id} — update task

DELETE /tasks/{id} — delete task

Day 2 — Authentication & Authorization (JWT)

Day 2 introduces user authentication, JWT-based authorization, and task ownership.
All task endpoints are protected and scoped to the authenticated user.

Features

User registration (/auth/register)

User login with JWT (/auth/login)

Password hashing with bcrypt

JWT access tokens

Protected routes using Depends

Task ownership enforcement

Centralized authorization logic

Authentication Flow

User registers with email and password

Password is hashed before storing in the database

User logs in and receives a JWT access token

Token is sent via Authorization: Bearer <token> header

Protected endpoints validate the token and resolve current_user

Auth Endpoints

Register user
POST /auth/register

Request body:
{
"email": "user@example.com
",
"password": "secret123"
}

Login user
POST /auth/login

Response:
{
"access_token": "jwt_token_here",
"token_type": "bearer"
}

Protected Task Endpoints

All task endpoints require authentication.

Authorization header:
Authorization: Bearer <access_token>

POST /tasks — create task (owned by current user)

GET /tasks — list own tasks

GET /tasks/{id} — get own task

PATCH /tasks/{id} — update own task

DELETE /tasks/{id} — delete own task

Security Notes

Passwords are never stored in plain text

Password length is validated before hashing (bcrypt 72-byte limit)

JWT tokens are verified on every protected request

Users cannot access or modify tasks owned by others

Day 3 — Authentication (JWT) & Testing
Overview

Day 3 focuses on hardening authentication and adding automated integration tests.
The API is now fully testable, isolated, and production-ready from an authentication perspective.

Authentication (JWT)
Login Flow

Authentication uses OAuth2 Password Flow

Passwords are hashed with bcrypt

On successful login, the API issues a JWT access token

Endpoints

POST /auth/register — register a new user

POST /auth/login — login and receive JWT token

The JWT sub claim stores the user’s email, which is later used to resolve the current user.

Authorization
Protected Endpoints

All task-related endpoints are protected using a centralized dependency:
Depends(get_current_user)

Protected endpoints:

POST /tasks

GET /tasks/

GET /tasks/{task_id}

PATCH /tasks/{task_id}

DELETE /tasks/{task_id}

Unauthorized requests return 401 Unauthorized.

Swagger Authorization

Swagger UI supports authentication via the Authorize button.

How to authorize in Swagger

Open Swagger UI:
http://localhost:8000/docs

Call POST /auth/login

Use form-data

username = email

password = password

Copy the returned access_token

Click Authorize (🔒 icon)

Paste:
Bearer <your_access_token>

All protected endpoints become accessible

Testing Setup
Test Stack

pytest

FastAPI TestClient

SQLite (isolated test database)

Tests are located in the tests/ directory and do not use Postgres or Docker.

Key Concepts

dependency_overrides replaces the real database with a test database

Tables are created and dropped automatically per test session

Tests simulate real HTTP requests against the API

Running Tests

Run tests from the project root:

python -m pytest -q

Example output:
5 passed, 1 warning in 3.9s

Covered Test Cases
Authentication Tests

User registration success

Duplicate email registration → 400

Successful login → JWT token returned

Wrong password → 401

Unknown user → 401

Task Tests

Access without token → 401

Create task

List tasks

Get task by ID

Update task

Delete task

Get deleted task → 404

Database & Architecture Notes

SQLAlchemy Base is declared separately to avoid circular imports

Models are registered via a dedicated module during test initialization

Test database is fully isolated from production data

Result (End of Day 3)

JWT authentication is fully functional

Task endpoints are properly secured

Swagger supports authorization

Integration tests are automated and isolated

The project has a solid production-ready foundation
