from datetime import timedelta, datetime
from typing import Type

from fastapi import Response, HTTPException, status
from src.auth.auth_settings import annotation_oauth2
from src.repositories.token_repository import AccessTokenRepository, RefreshTokenRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import RegisterSchema


class UserService:

    def __init__(self, user_repo: Type[UserRepository],access_token_repo: Type[AccessTokenRepository] = None,
                 refresh_token_repo: Type[RefreshTokenRepository] = None):
        self.user_repo = user_repo
        self.access_token_repo = access_token_repo
        self.refresh_token_repo = refresh_token_repo

    async def register_user(self, register_data: RegisterSchema):
        await self.user_repo().create_user(register_request=register_data)

    async def login_user(self, form_data: annotation_oauth2,  response: Response):
        user = await self.user_repo().authenticate_user(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        access_token_expires = timedelta(minutes=20)
        refresh_token_expires = timedelta(days=60)
        access_token = await self.access_token_repo().create_access_token(
            user.username, user.id, access_token_expires
        )
        refresh_token, jti = await self.refresh_token_repo().create_refresh_token(user.id, refresh_token_expires)
        expires_at = datetime.utcnow() + refresh_token_expires
        await self.refresh_token_repo().store_refresh_token(user.id, jti, expires_at)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=refresh_token_expires.seconds,
            path="/auth/refresh"
        )
        return access_token