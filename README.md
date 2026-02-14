# Task Management API

Backend-first REST API for managing tasks, built with **FastAPI** and **PostgreSQL**.

This project is developed incrementally as a multi-day backend-focused exercise.
Each part introduces new architectural concepts and production-ready features.

---

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Alembic** (database migrations)
- **Docker / docker-compose**
- **Pydantic**
- **JWT** (OAuth2 Password Flow)
- **pytest**

---

## Project Structure

TASK-MANAGEMENT-API/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── base_models.py
│   │   └── deps.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
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

Create a .env file in the project root (you can copy from .env.example).

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
- Swagger UI (`/docs`)
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
- Protected task routes using Depends(get_current_user)
- Task ownership (users can access only their own tasks) 

### Authentication Endpoints
### Register user 
POST /auth/register
    Content-Type: application/json 

{
  "email": "user@example.com",
  "password": "secret123"
}

### Login user
POST /auth/login
    Content-Type: application/x-www-form-urlencoded

Form fields:

- username — user email
- password — user password

Response:

{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}

### Swagger Authorization (How to use protected endpoints)

1) Open Swagger UI
    http://localhost:8000/docs

2) Call POST /auth/login
    - Enter username (email)
    - Enter password
    - Click Execute
    - Copy access_token

3) Click Authorize (🔒)

4) Paste:

    Bearer <your_access_token>

5) All protected /tasks endpoints are now accessible.

---

## Authentication & Testing

- OAuth2 Password Flow (JWT)
- Centralized `get_current_user` dependency
- Swagger authorization support
- Integration tests with pytest
- Isolated SQLite test database

### Running tests

Run tests from the project root:

    python -m pytest -q

Example output:

    5 passed, 1 warning in 3.9s

### Covered Test Cases
**Authentication**

- User registration success
- Duplicate email → 400
- Successful login → JWT token returned
- Wrong password → 401
- Unknown user → 401

**Tasks**

- Access without token → 401
- Create task
- List tasks
- Get task by ID
- Update task
- Delete task
- Get deleted task → 404


### Result 

- JWT authentication fully implemented
- Task endpoints secured
- Swagger supports authorization
- Integration tests automated and isolated
- Production-ready backend foundation

---

## Task Ownership & Authorization

### Goal
Implement **strict task ownership** with proper authorization rules, database-level constraints, and integration tests.

Only the task owner can:
- view a task
- update a task
- delete a task

---

### Implemented Features

#### 🔐 Task Ownership
- Each task belongs to a specific user via `user_id`
- Ownership enforced at:
  - **Database level** (Foreign Key + CASCADE)
  - **API level** (403 Forbidden)

sql
tasks.user_id → users.id (ON DELETE CASCADE) 

### 🚫 Authorization Rules (403 vs 404) 
| Case                                    | Response        |
| --------------------------------------- | --------------- |
| Task does not exist                     | `404 Not Found` |
| Task exists but belongs to another user | `403 Forbidden` |
| Task belongs to current user            | ✅ Allowed      |

### 📌 Protected Endpoints

All task endpoints require authentication (JWT):
- POST /tasks — create task (auto-assigns owner)
- GET /tasks — list only own tasks
- GET /tasks/{id} — only if owner
- PATCH /tasks/{id} — only if owner
- DELETE /tasks/{id} — only if owner

Example: Ownership Check (API) 

    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions") 

### Integration Tests (PostgreSQL)

- Tests run against real PostgreSQL (not SQLite)
- Database cleaned before each test: 

    TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;
    TRUNCATE TABLE users RESTART IDENTITY CASCADE;
- Ensures:
    - No state leakage between tests
    - Real FK & CASCADE behavior
    - Production-like environment

### Ownership Test Coverage
The API enforces strict resource ownership. Any attempt to access or modify a task owned by another user results in a 403 Forbidden response, while requests for non-existent resources correctly return 404 Not Found.

### Running Tests

    docker compose exec api python -m pytest -q

All tests pass successfully.

### Result

✅ Secure multi-user task isolation
✅ Clear authorization rules
✅ Database-level data integrity
✅ Production-ready test setup

---

## CI & Reliability

### What was implemented
- Dockerized PostgreSQL environment
- Alembic migrations
- Integration tests with real PostgreSQL
- Ownership enforcement (403 vs 404)
- GitHub Actions CI pipeline (runs on every push/PR)

### Run tests locally (Docker)
```bash
docker-compose up --build
docker-compose exec api alembic upgrade head
docker-compose exec api pytest -q 

CI

Workflow: .github/workflows/ci.yml

Steps: start PostgreSQL → run Alembic migrations → run pytest 

