from fastapi import Depends
from typing import Annotated

from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


def task_service():
    return TaskService(TaskRepository)

task_dependency = Annotated[TaskService,Depends(task_service)]