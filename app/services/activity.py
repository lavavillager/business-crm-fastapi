from sqlalchemy.orm import Session

from app.models.activity import ActivityLog
from app.repositories.activity import ActivityRepository


class ActivityService:
    def __init__(self, db: Session) -> None:
        self.repo = ActivityRepository(db)

    def log(
        self,
        *,
        user_id: int | None,
        action: str,
        entity: str,
        entity_id: int | None = None,
        detail: str | None = None,
    ) -> ActivityLog:
        entry = ActivityLog(
            user_id=user_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            detail=detail,
        )
        return self.repo.create(entry)

    def list(self, user_id: int | None, limit: int, offset: int):
        return self.repo.list_by_user(user_id, limit, offset)
