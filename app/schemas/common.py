from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """Универсальный ответ с пагинацией."""

    items: list[T]
    total: int
    limit: int
    offset: int
