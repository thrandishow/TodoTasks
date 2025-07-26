from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.auth.auth_settings import annotation_oauth2, token_annotation
from src.db.database import db_dependency
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, TokenSchema
from src.services.dependencies import user_service_dependency_auth, user_service_dependency


router = APIRouter(prefix="/auth", tags=["Auth"])

user_dependency = Annotated[dict, Depends(UserRepository.get_current_user)]


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return {"user": user}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        register_data: RegisterSchema, user_service_dep: user_service_dependency
) -> Response:
    await user_service_dep.register_user(register_data)
    return Response(content="User created")


@router.post("/token", response_model=TokenSchema)
async def login_for_tokens(form_data: annotation_oauth2,
        user_service_dep: user_service_dependency_auth,
        response: Response = None):
    access_token = await user_service_dep.login_user(form_data,response)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token(refresh_token: token_annotation, db: db_dependency):
    pass
