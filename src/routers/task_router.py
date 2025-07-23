from fastapi import APIRouter, status, Response, HTTPException
from fastapi.responses import JSONResponse

from src.database import db_dependency
from src.repositories.task_repository import TaskRepository
from src.schemas.task_schema import TaskAdd, Task, TaskPutRequest

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(db: db_dependency) -> dict[str, list[Task]]:
    tasks = await TaskRepository.find_all(db)
    return {"data": tasks}


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_one_task(task: TaskAdd, db: db_dependency) -> dict[str, int]:
    task_id = await TaskRepository.add_one(task, db)
    return {"id": task_id}


@router.delete("/{task_id}/")
async def remove_task(task_id: int, db: db_dependency):
    result = await TaskRepository.remove_task_by_id(task_id, db)
    if result:
        return Response(content="Task was deleted", status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(detail="Task not found", status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{task_id}/")
async def change_task(task_id: int, data_for_change: TaskPutRequest, db: db_dependency):
    updated_task = await TaskRepository.change_task_by_id(task_id, data_for_change, db)
    if updated_task:
        return JSONResponse(content={"message": "Task was updated", "data": updated_task},
                            status_code=status.HTTP_200_OK)
    raise HTTPException(detail="Task was not found", status_code=status.HTTP_404_NOT_FOUND)
