# Task Management API

Backend-first REST API for managing tasks, built with **FastAPI** and **PostgreSQL**.

This project is developed incrementally as a backend-focused exercise and demonstrates
production-ready API design, authentication, authorization, testing, and CI practices.

---

## CI Status

- ✅ All checks passing (green)
- ✅ Tests, migrations, and coverage verified on every push and pull request
- ✅ Minimum test coverage enforced: **≥ 85%**

---

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Alembic** (database migrations)
- **Docker / Docker Compose**
- **Pydantic**
- **JWT** (OAuth2 Password Flow)
- **pytest**
- **GitHub Actions (CI)**

---

## Project Structure

TASK-MANAGEMENT-API/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── base_models.py
│   │   └── deps.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── auth_schemas.py
│   └── router/
│       ├── auth.py
│       ├── tasks.py
│       └── deps_auth.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── alembic/
│   ├── versions/
│   └── env.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env
├── .env.example
├── alembic.ini
└── README.md

---

## Requirements

- Docker + Docker Compose
- Python 3.11+ (required only for running tests locally)

## Environment Variables

Create a `.env` file in the project root (you can copy from `.env.example`).

Example: 
    DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres
    SECRET_KEY=change_me_to_a_long_random_secret 

## Running the Project (Docker)
1) Start containers
    docker-compose up --build

2) Apply database migrations
    docker-compose exec api alembic upgrade head

3) Open Swagger UI
    http://localhost:8000/docs

## Core API & Database Setup

- Task CRUD endpoints
- PostgreSQL integration
- SQLAlchemy 2.0 ORM models
- Alembic migrations
- Interactive API documentation via Swagger
- Fully Dockerized local environment

## Example Endpoints

- POST /tasks — create task
- GET /tasks/ — list tasks
- GET /tasks/{id} — get task by id
- PATCH /tasks/{id} — update task
- DELETE /tasks/{id} — delete task

---

## Authentication & Authorization (JWT)

It introduces user authentication, JWT-based authorization, and protected endpoints.

### Features

- User registration (POST /auth/register)
- User login (POST /auth/login)
- Password hashing with bcrypt
- JWT access tokens
- OAuth2 Password Flow
- Centralized get_current_user dependency
- Protected task endpoints 

### Swagger Authorization (How to use protected endpoints)

1) Open Swagger UI
    http://localhost:8000/docs

2) Call POST /auth/login
    - username → email
    - password → password

3) Copy access_token

4) Click Authorize and paste:

    Bearer <your_access_token>

## Task Ownership & Authorization

### Goal
Implement **strict task ownership** with proper authorization rules, database-level constraints, and integration tests.

Only the task owner can:
- view a task
- update a task
- delete a task

### Ownership Implementation
- Each task belongs to a specific user via `user_id`
- Ownership enforced at:
  - **Database level** (Foreign Key + CASCADE)
  - **API level** (authorization checks)

SQL
    tasks.user_id → users.id (ON DELETE CASCADE) 

---

### 🚫 Authorization Rules (403 vs 404) 
| Case                                    | Response        |
| --------------------------------------- | --------------- |
| Task does not exist                     | `404 Not Found` |
| Task exists but belongs to another user | `403 Forbidden` |
| Task belongs to current user            | ✅ Allowed      |

---

#### Example: Ownership Check (API) 

    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions") 

--- 

## Testing & CI
#### Test Setup

- Integration tests with real PostgreSQL (Docker)

- Alembic migrations applied before tests

- Database cleaned before each test run:

    TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;
    TRUNCATE TABLE users RESTART IDENTITY CASCADE;

- JWT authentication tested with real tokens

- Full coverage of ownership rules (401 / 403 / 404)

--- 

## Run Tests (Docker)

    docker-compose exec api pytest -q 

--- 

## Coverage

- Test coverage enforced at ≥ 85%

- Coverage checked automatically in CI

- Build fails if coverage threshold is not met 

--- 

## CI Pipeline (GitHub Actions)

On every ***push*** and ***pull request***, CI:

1. Builds Docker containers

2. Starts PostgreSQL

3. Applies Alembic migrations

4. Runs pytest with coverage

5. Fails on test, migration, or coverage errors

This guarantees:

- Clean, reproducible test environment

- No dependency on local setup

- Protection against untested code

--- 

## Result

✅ Secure multi-user task isolation

✅ Clear authorization rules (401 / 403 / 404)

✅ Database-level data integrity

✅ High test coverage with CI enforcement

✅ Production-ready backend foundation
