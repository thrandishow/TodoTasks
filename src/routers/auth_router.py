from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.auth.auth_settings import annotation_oauth2, token_annotation
from src.database import db_dependency
from src.repositories.token_repository import TokenRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema, TokenSchema

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
) -> Response:
    await UserRepository.create_user(register_data, db)
    return Response(content="User created")


@router.post("/token", response_model=TokenSchema)
async def login_for_tokens(form_data: annotation_oauth2, db: db_dependency, response: Response = None):
    user = await UserRepository.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    access_token_expires = timedelta(minutes=20)
    refresh_token_expires = timedelta(days=60)
    access_token = await TokenRepository.create_access_token(
        user.username, user.id, access_token_expires
    )
    refresh_token, jti = await TokenRepository.create_refresh_token(user.id, refresh_token_expires)
    expires_at = datetime.utcnow() + refresh_token_expires
    await TokenRepository.store_refresh_token(user.id, jti, expires_at, db)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=refresh_token_expires.seconds,
        path="/auth/refresh"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token(refresh_token: token_annotation, db: db_dependency):
    pass
