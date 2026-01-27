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

---

## Features (Day 1)

- CRUD operations for tasks
- Pydantic request/response schemas
- PostgreSQL database integration
- Alembic migrations
- Swagger UI (`/docs`)
- Dockerized local development

---

## Project Structure

```text
app/
  main.py
  core/config.py
  db/session.py
  db/base.py
  models/task.py
  schemas/task.py
  routers/tasks.py
alembic/
Dockerfile
docker-compose.yml
requirements.txt 