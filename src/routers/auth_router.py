from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, RegisterResponseSchema, TokenSchema
from src.database import db_dependency
from src.auth.auth_settings import annotation_oauth2

router = APIRouter(prefix="/auth", tags=["Auth"])

user_dependency = Annotated[dict, Depends(UserRepository.get_current_user)]


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return {"user": user}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_data: RegisterSchema, db: db_dependency
) -> RegisterResponseSchema:
    await UserRepository.create_user(register_data, db)
    return {"message": "Successful user registration"}


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: annotation_oauth2, db: db_dependency):
    user = await UserRepository.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    token = await UserRepository.create_access_token(
        user.username, user.id, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
