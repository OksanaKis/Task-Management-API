from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: str = Field(default="todo")
    priority: str = Field(default="medium")

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: str | None = None
    priority: str | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str

    model_config = {"from_attributes": True}
