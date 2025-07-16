from typing import Optional
from pydantic import BaseModel


class TaskAdd(BaseModel):
    name: str
    description: Optional[str] = None


class Task(TaskAdd):
    id: int
