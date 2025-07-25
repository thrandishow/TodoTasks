import jwt
from fastapi import HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth_settings import (
    bcrypt_context,
    token_annotation,
)
from src.auth.config import ALGORITHM, SECRET_KEY
from src.models.user_model import UserOrm
from src.schemas.auth_schema import RegisterSchema


class UserRepository:
    @classmethod
    async def create_user(cls, register_request: RegisterSchema, db: AsyncSession):
        user_model = UserOrm(
            username=register_request.username,
            email=register_request.email,
            password=bcrypt_context.hash(register_request.password),
        )
        db.add(user_model)
        await db.commit()

    @classmethod
    async def authenticate_user(cls, username: str, password: str, db: AsyncSession):
        user = await db.execute(
            select(UserOrm).where(UserOrm.username == username)
        )
        user = user.scalar_one()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False
        return user

    @classmethod
    async def get_current_user(cls, access_token: token_annotation):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: str = payload.get("id")
            if username is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate user",
                )
            return {"username": username, "id": user_id}
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
            )
