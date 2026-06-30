from sqlalchemy import func, select

from app.models.activity import ActivityLog
from app.repositories.base import BaseRepository


class ActivityRepository(BaseRepository[ActivityLog]):
    model = ActivityLog

    def list_by_user(
        self, user_id: int | None, limit: int, offset: int
    ) -> tuple[list[ActivityLog], int]:
        stmt = select(ActivityLog)
        count_stmt = select(func.count()).select_from(ActivityLog)
        if user_id is not None:
            stmt = stmt.where(ActivityLog.user_id == user_id)
            count_stmt = count_stmt.where(ActivityLog.user_id == user_id)
        total = self.db.scalar(count_stmt) or 0
        stmt = stmt.order_by(ActivityLog.created_at.desc()).limit(limit).offset(offset)
        return list(self.db.scalars(stmt).all()), total
