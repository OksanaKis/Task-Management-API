from fastapi import FastAPI
from app.router.tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])