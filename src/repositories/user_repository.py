from src.database import new_session
from src.schemas.auth_schema import RegisterSchema
from src.models.user_model import UserOrm
from src.auth.auth_settings import bcrypt_context
from src.database import db_dependency


class UserRepository:
    @classmethod
    async def create_user(
        cls,
        register_user_request: RegisterSchema,
        db: db_dependency,
    ):
        async with new_session() as session:
            user_model = UserOrm(
                username=register_user_request.username,
                email=register_user_request.email,
                password=bcrypt_context.hash(register_user_request.password),
            )
            session.add(user_model)
            await session.commit()
