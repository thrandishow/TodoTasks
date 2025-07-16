from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskId(BaseModel):
    status_code: int
    id: int


class TaskListResponse(BaseModel):
    data: list[Task]
    status_code: int = 200
