from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.database import Base
from src.models.user_model import UserOrm


class RefreshTokenOrm(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    jti: Mapped[str] = mapped_column(unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="refresh_tokens")
