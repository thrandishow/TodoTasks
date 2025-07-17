from fastapi import APIRouter, status
from .repositories.task_repository import TaskRepository
from src.schemas.task_schema import TaskAdd, TaskId, TaskListResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks() -> TaskListResponse:
    tasks = await TaskRepository.find_all()
    return {"data": tasks}


@router.post("", status_code=status.HTTP_200_OK)
async def add_one_task(task: TaskAdd) -> TaskId:
    task_id = await TaskRepository.add_one(task)
    return {"id": task_id}
