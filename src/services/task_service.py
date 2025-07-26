from typing import Type

from src.repositories.task_repository import TaskRepository
from src.schemas.task_schema import TaskAdd, TaskPutRequest


class TaskService:
    def __init__(self,tasks_repo: Type[TaskRepository]):
        self.tasks_repo = tasks_repo

    async def get_all_tasks(self):
        tasks = await self.tasks_repo().find_all()
        return tasks

    async def add_one_task(self, data: TaskAdd):
        task_id = await self.tasks_repo().add_one_task(data)
        return task_id

    async def remove_task(self, task_id: int):
        result = await self.tasks_repo().remove_task_by_id(task_id)
        return result

    async def update_task(self, data_for_change: TaskPutRequest):
        updated_task = await self.tasks_repo().change_task_by_id(data_for_change)
        return updated_task