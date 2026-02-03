# Task Management API

Backend-first REST API for managing tasks, built with **FastAPI** and **PostgreSQL**.

This project is developed incrementally.  
**Day 1** focuses on core API structure, database setup, and Dockerized development environment.

---

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Alembic** (database migrations)
- **Docker / docker-compose**
- **Pydantic**

---

## Features (Day 1)

- Task CRUD endpoints
- Request & response validation with Pydantic
- PostgreSQL database integration
- SQLAlchemy 2.0 ORM models
- Alembic migrations
- Swagger UI (`/docs`)
- Fully Dockerized local environment

---

```md
## Project Structure

```text
app/
  main.py
  core/config.py
  db/session.py
  db/base.py
  models/task.py
  schemas/task.py
  router/tasks.py
alembic/
Dockerfile
docker-compose.yml
requirements.txt 
```

## Running the Project (Day 1)

1️⃣ Start containers
docker-compose up --build
2️⃣ Apply database migrations
docker-compose exec api alembic upgrade head
3️⃣ Open API documentation

## Swagger UI:
👉 http://localhost:8000/docs

Example Endpoints (Day 1)
- POST /tasks — create task
- GET /tasks — list tasks
- GET /tasks/{id} — get task by id
- PATCH /tasks/{id} — update task
- DELETE /tasks/{id} — delete task

--- 

# Day 2 — Authentication & Authorization (JWT)

Day 2 focuses on implementing user authentication, JWT-based authorization, and task ownership.
All task-related endpoints are now protected and scoped to the authenticated user.

## Features (Day 2)

- User registration (/auth/register)
- User login with JWT (/auth/login)
- Password hashing with bcrypt
- JWT access tokens
- Protected routes using Depends
- Task ownership (users can only access their own tasks)
- Secure authorization flow

## Authentication Flow

- User registers with email and password
- Password is hashed before storing in the database
- User logs in and receives a JWT access token
- Token is sent via Authorization: Bearer <token> header
- Protected endpoints validate the token and extract current_user

## Project Structure (Day 2)
app/
  main.py
  core/
    config.py
    security.py
  db/
    session.py
    base.py
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
alembic/
Dockerfile
docker-compose.yml
requirements.txt

## Running the Project (Day 2)
1. Start containers
docker-compose up --build

2. Apply database migrations
docker-compose exec api alembic upgrade head

3. Open API documentation

## Swagger UI:
👉 http://localhost:8000/docs

## Auth Endpoints (Day 2)
### Register user

POST /auth/register
{
  "email": "user@example.com",
  "password": "secret123"
}

### Login user

POST /auth/login
Response:
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}

### Protected Task Endpoints

All task endpoints require authentication.

### Authorization header
Authorization: Bearer <access_token>

## Endpoints

- POST /tasks — create task (owned by current user)
- GET /tasks — list own tasks
- GET /tasks/{id} — get own task
- PATCH /tasks/{id} — update own task
- DELETE /tasks/{id} — delete own task

### Security Notes

- Passwords are never stored in plain text
- Password length is validated before hashing (bcrypt 72-byte limit)
- JWT tokens are verified on every protected request
- Users cannot access or modify tasks owned by others