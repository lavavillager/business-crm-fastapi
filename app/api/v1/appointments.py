from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import AppointmentStatus, UserRole
from app.db.session import get_db
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)
from app.schemas.common import Page
from app.services.activity import ActivityService
from app.services.appointment import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Записи"])


@router.get(
    "",
    response_model=Page[AppointmentRead],
    summary="Список / фильтрация записей",
)
def list_appointments(
    status_filter: AppointmentStatus | None = Query(
        None, alias="status", description="Фильтр по статусу записи"
    ),
    date_from: datetime | None = Query(None, description="Записи начиная с даты"),
    date_to: datetime | None = Query(None, description="Записи до даты"),
    client_id: int | None = Query(None),
    employee_id: int | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Page[AppointmentRead]:
    items, total = AppointmentService(db).search(
        status=status_filter,
        date_from=date_from,
        date_to=date_to,
        client_id=client_id,
        employee_id=employee_id,
        limit=limit,
        offset=offset,
    )
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{appointment_id}", response_model=AppointmentRead, summary="Получить запись")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> AppointmentRead:
    return AppointmentService(db).get_or_404(appointment_id)


@router.post(
    "",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать запись",
)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    appointment = AppointmentService(db).create(data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="create",
        entity="appointment",
        entity_id=appointment.id,
    )
    return appointment


@router.patch(
    "/{appointment_id}", response_model=AppointmentRead, summary="Обновить запись / статус"
)
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    appointment = AppointmentService(db).update(appointment_id, data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="update",
        entity="appointment",
        entity_id=appointment_id,
    )
    return appointment


@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить запись (admin/manager)",
)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> None:
    AppointmentService(db).delete(appointment_id)
    ActivityService(db).log(
        user_id=current_user.id,
        action="delete",
        entity="appointment",
        entity_id=appointment_id,
    )
