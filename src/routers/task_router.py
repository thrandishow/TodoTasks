from fastapi import APIRouter, status
from src.repositories.task_repository import TaskRepository
from src.schemas.task_schema import TaskAdd, TaskId, TaskListResponse
from src.database import db_dependency

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(db: db_dependency) -> TaskListResponse:
    tasks = await TaskRepository.find_all(db)
    return {"data": tasks}


@router.post("", status_code=status.HTTP_200_OK)
async def add_one_task(task: TaskAdd, db: db_dependency) -> TaskId:
    task_id = await TaskRepository.add_one(task, db)
    return {"id": task_id}
