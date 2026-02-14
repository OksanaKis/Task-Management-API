import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import app.db.base_models  # noqa: F401
from app.db.base import Base
from app.db.deps import get_db
from app.main import app as fastapi_app

app: FastAPI = fastapi_app

# Використовуємо ту ж БД, що й контейнер (tasks_db)
# Можеш винести в env, але так працює одразу.
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/tasks_db",
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    # На Postgres таблиці створюються міграціями/metadata.
    # Для тестів найпростіше: створити таблиці один раз.
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_db():
    # ВАЖЛИВО: чистимо між тестами, щоб не було витоків стану
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()