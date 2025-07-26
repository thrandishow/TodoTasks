from fastapi import APIRouter, status, Response, HTTPException
from fastapi.responses import JSONResponse

from src.schemas.task_schema import TaskAdd, Task, TaskPutRequest
from src.services.dependencies import task_dependency

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_tasks(task_service: task_dependency) -> dict[str, list[Task]]:
    tasks = await task_service.get_all_tasks()
    return {"data": tasks}


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_one_task(task: TaskAdd,task_service: task_dependency) -> dict[str, int]:
    task_id = await task_service.add_one_task(task)
    return {"id": task_id}


@router.delete("/{task_id}/")
async def remove_task(task_id: int,task_service: task_dependency):
    result = await task_service.remove_task(task_id)
    if result:
        return Response(content="Task was deleted", status_code=status.HTTP_200_OK)
    raise HTTPException(detail="Task not found", status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{task_id}/")
async def change_task(data_for_change: TaskPutRequest, task_service: task_dependency):
    updated_task = await task_service.update_task(data_for_change)
    if updated_task:
        return JSONResponse(content={"message": "Task was updated", "data": updated_task},
                            status_code=status.HTTP_200_OK)
    raise HTTPException(detail="Task was not found", status_code=status.HTTP_404_NOT_FOUND)
