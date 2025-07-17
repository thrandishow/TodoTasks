from typing import Optional
from fastapi import status
from pydantic import BaseModel, ConfigDict


class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskId(BaseModel):
    id: int


class TaskListResponse(BaseModel):
    data: list[Task]
