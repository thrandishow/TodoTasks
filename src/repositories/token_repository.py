import uuid
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, status
from sqlalchemy import select, delete

from src.auth.auth_settings import token_annotation
from src.auth.config import SECRET_KEY, ALGORITHM
from src.database import db_dependency, new_session
from src.models.token_model import RefreshTokenOrm


class TokenRepository:
    @classmethod
    async def create_access_token(cls, username, user_id, expires_delta: timedelta):
        encode = {"sub": username, "id": user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    async def create_refresh_token(cls, user_id, expires_delta: timedelta):
        jti = str(uuid.uuid4())
        expires = datetime.utcnow() + expires_delta
        encode = {"sub": str(user_id), "jti": jti, "exp": expires}
        refresh_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return refresh_token, jti

    @classmethod
    async def create_access_token_from_refresh_token(cls, refresh_token: token_annotation):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username")
            user_id = payload.get("user_id")
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @classmethod
    async def store_refresh_token(cls, user_id: int, jti: str, expires_at: datetime, db: db_dependency):
        async with new_session() as session:
            refresh_token = RefreshTokenOrm(
                user_id=user_id, jti=jti, expires_at=expires_at
            )
            session.add(refresh_token)
            await session.commit()

    @classmethod
    async def get_refresh_token(cls, user_id: int, jti: str, db: db_dependency):
        async with new_session() as session:
            query = select(RefreshTokenOrm).where(RefreshTokenOrm.jti == jti, RefreshTokenOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def delete_refresh_token(cls, jti: str, db: db_dependency):
        async with new_session() as session:
            query = delete(RefreshTokenOrm).where(RefreshTokenOrm.jti == jti)
            await session.execute(query)
            await session.commit()
