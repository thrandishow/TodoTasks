from fastapi import APIRouter, status
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, RegisterResponseSchema
from src.database import db_dependency


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_data: RegisterSchema, db: db_dependency
) -> RegisterResponseSchema:
    await UserRepository.create_user(register_data, db)
    return {"message": "Successful user registration"}
