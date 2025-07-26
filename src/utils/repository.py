from abc import ABC

from src.db.database import Base


class AbstractRepository(ABC):
    model: Base

