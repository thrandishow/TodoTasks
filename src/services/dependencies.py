from fastapi import Depends
from typing import Annotated

from src.repositories.task_repository import TaskRepository
from src.repositories.token_repository import AccessTokenRepository, RefreshTokenRepository
from src.repositories.user_repository import UserRepository
from src.services.task_service import TaskService
from src.services.user_service import UserService


def task_service():
    return TaskService(TaskRepository)

def user_service():
    return UserService(UserRepository)

def user_service_auth():
    return UserService(UserRepository,AccessTokenRepository,RefreshTokenRepository)

task_dependency = Annotated[TaskService,Depends(task_service)]
user_service_dependency = Annotated[UserService,Depends(user_service)]
user_service_dependency_auth = Annotated[UserService,Depends(user_service_auth)]