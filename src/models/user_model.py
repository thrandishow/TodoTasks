from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    refresh_token = relationship("RefreshTokenOrm",backref="user",uselist=False)
