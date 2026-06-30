from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import Page
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.services.activity import ActivityService
from app.services.service import ServiceService

router = APIRouter(prefix="/services", tags=["Услуги"])


@router.get("", response_model=Page[ServiceRead], summary="Список услуг")
def list_services(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Page[ServiceRead]:
    items, total = ServiceService(db).list(limit, offset)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{service_id}", response_model=ServiceRead, summary="Получить услугу")
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ServiceRead:
    return ServiceService(db).get_or_404(service_id)


@router.post(
    "",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать услугу (admin/manager)",
)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> ServiceRead:
    service = ServiceService(db).create(data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="create",
        entity="service",
        entity_id=service.id,
    )
    return service


@router.patch(
    "/{service_id}", response_model=ServiceRead, summary="Обновить услугу (admin/manager)"
)
def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> ServiceRead:
    service = ServiceService(db).update(service_id, data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="update",
        entity="service",
        entity_id=service_id,
    )
    return service


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить услугу (admin)",
)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
) -> None:
    ServiceService(db).delete(service_id)
    ActivityService(db).log(
        user_id=current_user.id,
        action="delete",
        entity="service",
        entity_id=service_id,
    )
