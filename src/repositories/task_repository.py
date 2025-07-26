from sqlalchemy import select, update

from src.db.database import session_manager
from src.models.task_model import TaskOrm
from src.schemas.task_schema import Task, TaskAdd, TaskPutRequest
from src.utils.repository import AbstractRepository


class TaskRepository(AbstractRepository):
    """Methods for work with Tasks"""
    model = TaskOrm

    async def add_one_task(self, data: TaskAdd) -> int:
        """
        Add one task to database.

        Args:
            data (TaskAdd): Contains data task for adding in database

        Returns:
            Task id that was given to it, if operation was successful.
        """
        async with session_manager() as session:
            task_dict = data.model_dump()

            task = self.model(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()

        return task.id


    async def find_all(self) -> list[Task]:
        """
        Returns all tasks in database.

        Returns:
            List of all tasks in database.
        TODO: Make tasks only for authenticated users
        """
        async with session_manager() as session:
            query = select(self.model)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [
                Task.model_validate(task_model) for task_model in task_models
            ]
            return task_schemas


    async def remove_task_by_id(self, task_id: int) -> bool:
        """
        Removes task by id, if it exists.

        Args:
            task_id (int): ID of task

        Returns:
            True if operation successful, False if task not found.
        """
        async with session_manager() as session:
            task = await session.get(self.model, task_id)
            if task is None:
                return False
            await session.delete(task)
            await session.commit()
            return True


    async def change_task_by_id(self, data_for_change: TaskPutRequest) -> None | Task:
        """
        Changes all data of task in database.

        Args:
            data_for_change: Data for changing name and description of task

        Returns:
            Changed task if task was found and changed, else None.
        """
        async with session_manager() as session:
            task = await session.get(self.model, data_for_change.task_id)
            if task is None:
                return None
            update(task).values(**data_for_change)
            await session.flush()
            await session.commit()
            return Task.model_validate(task).model_dump()
