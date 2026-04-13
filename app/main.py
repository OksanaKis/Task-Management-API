from fastapi import FastAPI

from app.router.auth import router as auth_router
from app.router.tasks import router as tasks_router

app = FastAPI(
    title="Task Management API",
    description="Backend API with JWT authentication, task ownership, PostgreSQL, Docker, and CI",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(tasks_router)