import jwt
from fastapi import HTTPException, status
from sqlalchemy import select

from src.auth.auth_settings import (
    bcrypt_context,
    token_annotation,
)
from src.auth.config import ALGORITHM, SECRET_KEY
from src.db.database import session_manager
from src.models.user_model import UserOrm
from src.schemas.auth_schema import RegisterSchema
from src.utils.repository import AbstractRepository


class UserRepository(AbstractRepository):
    """Methods for work with User"""
    model = UserOrm

    async def create_user(self, register_request: RegisterSchema):
        """
        Adds user in database, hashing password for security.

        Args:
            register_request (RegisterSchema): Required fields (username,password,email)
        """
        async with session_manager() as session:
            user_model = self.model(
                username=register_request.username,
                email=register_request.email,
                password=bcrypt_context.hash(register_request.password),
            )
            session.add(user_model)
            await session.commit()

    async def authenticate_user(self, username: str, password: str):
        """
        Authenticates user.

        Args:
            username (str): user's username
            password: user's password

        Returns:
            False if user not found in database or hashes of passwords in request and database not equal,
            if all successful returns user.
        """
        async with session_manager() as session:
            user = await session.execute(
                select(self.model).where(self.model.username == username)
            )
            user = user.scalar_one()
            if not user:
                return False
            if not bcrypt_context.verify(password, user.password):
                return False
            return user

    @staticmethod
    async def get_current_user(access_token: token_annotation):
        """
        Returns user's data if authenticated.

        Args:
            access_token (oauth2_bearer): token of authenticated user

        Returns:
            User data if no exceptions and all data is correct and exists (dict).
            {"username": str,"user_id": int}

        Raises:
            HTTPException: status_code - 401 (Unauthorized), could not validate user.
        """
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
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
