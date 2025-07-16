from fastapi import APIRouter
from .repositories.repository import TaskRepository
from src.schemas.schema import TaskAdd, TaskId, TaskListResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def get_all_tasks() -> TaskListResponse:
    tasks = await TaskRepository.find_all()
    return {"data": tasks, "status_code": 200}


@router.post("")
async def add_one_task(task: TaskAdd) -> TaskId:
    task_id = await TaskRepository.add_one(task)
    return {"id": task_id, "status_code": 200}
