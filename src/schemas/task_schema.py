from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


class Task(TaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    data: list[Task]


class TaskPutRequest(BaseModel):
    name: str
    description: str
