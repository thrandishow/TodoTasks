from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
