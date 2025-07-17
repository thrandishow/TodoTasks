from sqlalchemy import select
from src.database import new_session
from ..models.task_model import TaskOrm
from ..schemas.task_schema import Task, TaskAdd


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
    async def find_all(cls) -> list[Task]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [
                Task.model_validate(task_model) for task_model in task_models
            ]
            return task_schemas
