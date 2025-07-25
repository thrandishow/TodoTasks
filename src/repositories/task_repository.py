from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task_model import TaskOrm
from src.schemas.task_schema import Task, TaskAdd, TaskPutRequest


class TaskRepository:

    @classmethod
    async def add_one(cls, data: TaskAdd, db: AsyncSession) -> int:
        task_dict = data.model_dump()

        task = TaskOrm(**task_dict)
        db.add(task)
        await db.flush()
        await db.commit()

        return task.id

    @classmethod
    async def find_all(cls, db: AsyncSession) -> list[Task]:
        query = select(TaskOrm)
        result = await db.execute(query)
        task_models = result.scalars().all()
        task_schemas = [
            Task.model_validate(task_model) for task_model in task_models
        ]
        return task_schemas

    @classmethod
    async def remove_task_by_id(cls, task_id: int, db: AsyncSession) -> bool:
        task = await db.get(TaskOrm, task_id)
        if task is None:
            return False
        await db.delete(task)
        await db.commit()
        return True

    @classmethod
    async def change_task_by_id(cls, task_id: int, data_for_change: TaskPutRequest, db: AsyncSession) -> None | Task:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await db.execute(query)
            task = result.scalar_one_or_none()
            if result is None:
                return None
            task.name = data_for_change.name
            task.description = data_for_change.description
            await db.flush()
            await db.commit()
            return Task.model_validate(task).model_dump()
