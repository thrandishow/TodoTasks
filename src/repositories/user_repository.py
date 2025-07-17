from src.database import new_session, db_dependency
from src.schemas.auth_schema import CreateUserRequest
from src.models.user_model import UserOrm
from src.auth.auth_settings import bcrypt_context


class UserRepository:
    @classmethod
    async def create_user(
        cls, db: db_dependency, create_user_request: CreateUserRequest
    ):
        async with new_session() as session:
            create_user_model = UserOrm(
                username=create_user_request.username,
                password=bcrypt_context.hash(create_user_request.password),
            )
            session.add(create_user_model)
            await session.commit()
