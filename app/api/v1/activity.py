from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.schemas.activity import ActivityLogRead
from app.schemas.common import Page
from app.services.activity import ActivityService

router = APIRouter(prefix="/activity", tags=["История действий"])


@router.get(
    "",
    response_model=Page[ActivityLogRead],
    summary="История действий пользователей (admin/manager)",
)
def list_activity(
    user_id: int | None = Query(None, description="Фильтр по пользователю"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> Page[ActivityLogRead]:
    items, total = ActivityService(db).list(user_id, limit, offset)
    return Page(items=items, total=total, limit=limit, offset=offset)
