from sqlalchemy import select
from src.database import new_session, db_dependency
from src.models.task_model import TaskOrm
from src.schemas.task_schema import Task, TaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskAdd, db: db_dependency) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()

            return task.id

    @classmethod
    async def find_all(cls, db: db_dependency) -> list[Task]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [
                Task.model_validate(task_model) for task_model in task_models
            ]
            return task_schemas

    @classmethod
    async def remove_task_by_id(cls,task_id: int, db: db_dependency) -> None:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id==task_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            if result is None:
                return None
            session.delete(task)
            await session.commit()