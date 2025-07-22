from fastapi import APIRouter, status, Response, HTTPException
from src.repositories.task_repository import TaskRepository
from src.schemas.task_schema import TaskAdd, Task
from src.database import db_dependency

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(db: db_dependency) -> dict[str, list[Task]]:
    tasks = await TaskRepository.find_all(db)
    return {"data": tasks}


@router.post("", status_code=status.HTTP_200_OK)
async def add_one_task(task: TaskAdd, db: db_dependency) -> dict[str, int]:
    task_id = await TaskRepository.add_one(task, db)
    return {"id": task_id}

@router.delete("/{task_id}/")
async def remove_task(task_id: int,db: db_dependency):
    result = await TaskRepository.remove_task_by_id(task_id,db)
    if result:
        return Response(content="Task was deleted",status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(detail="Task not found",status_code=status.HTTP_404_NOT_FOUND)
