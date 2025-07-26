from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.db.db_settings import Setting

engine = create_async_engine(Setting.db_url, echo=True)
session_manager = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Return session"""
    db = session_manager()
    try:
        yield db
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()


async def init_models() -> None:
    """Initializing data"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    """Run tasks before and after the server starts."""
    await init_models()
    yield


db_dependency = Annotated[AsyncSession, Depends(get_db)]
