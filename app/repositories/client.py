from sqlalchemy import func, or_, select

from app.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    model = Client

    def search(
        self, query: str | None, limit: int, offset: int
    ) -> tuple[list[Client], int]:
        stmt = select(Client)
        count_stmt = select(func.count()).select_from(Client)
        if query:
            pattern = f"%{query}%"
            condition = or_(
                Client.name.ilike(pattern),
                Client.phone.ilike(pattern),
                Client.email.ilike(pattern),
            )
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)
        total = self.db.scalar(count_stmt) or 0
        stmt = stmt.order_by(Client.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all()), total
