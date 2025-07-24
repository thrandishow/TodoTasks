from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.token_model import RefreshTokenOrm


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    token: Mapped["RefreshTokenOrm"] = relationship("RefreshTokenOrm", back_populates="user")
