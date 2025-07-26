import uuid
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, status
from sqlalchemy import select, delete

from src.auth.auth_settings import token_annotation
from src.auth.config import SECRET_KEY, ALGORITHM
from src.db.database import session_manager
from src.models.token_model import RefreshTokenOrm
from src.utils.repository import AbstractRepository


class RefreshTokenRepository(AbstractRepository):
    """Methods for work with tokens"""
    model = RefreshTokenOrm

    @staticmethod
    async def create_refresh_token(user_id, expires_delta: timedelta):
        jti = str(uuid.uuid4())
        expires = datetime.utcnow() + expires_delta
        encode = {"sub": str(user_id), "jti": jti, "exp": expires}
        refresh_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return refresh_token, jti


    async def store_refresh_token(self, user_id: int, jti: str, expires_at: datetime):
        async with session_manager() as session:
            refresh_token = self.model(
                user_id=user_id, jti=jti, expires_at=expires_at
            )
            session.add(refresh_token)
            await session.commit()

    async def get_refresh_token(self, user_id: int, jti: str):
        async with session_manager() as session:
            query = select(self.model).where(
                self.model.jti == jti,
                self.model.user_id == user_id
            )
            result = await session.execute(query)
            return result.scalars().first()

    async def delete_refresh_token(self, jti: str):
        async with session_manager() as session:
            query = delete(self.model).where(self.model.jti == jti)
            await session.execute(query)
            await session.commit()


class AccessTokenRepository(AbstractRepository):
    """Methods for work with access token."""
    model = None

    @staticmethod
    async def create_access_token(username: str, user_id: int, expires_delta: timedelta):
        """
        Creates access token from user data.

        Args:
            username (str): Username of user
            user_id (int): ID of user
            expires_delta (timedelta): The time when token is expired

        Returns:
            Bearer token (JWT).
        """
        expires = datetime.utcnow() + expires_delta
        encode = {"sub": username, "id": user_id, "exp": expires}
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def create_access_token_from_refresh_token(refresh_token: token_annotation):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username")
            user_id = payload.get("user_id")
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")