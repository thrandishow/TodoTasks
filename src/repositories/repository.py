from typing import Sequence
from sqlalchemy import select
from config.database.db_helper import new_session
from src.models.task_model import TaskOrm
from src.schemas.task_schema import Task, TaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()

            return task.id

    @classmethod
    async def find_all(cls) -> Sequence[TaskOrm]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models
