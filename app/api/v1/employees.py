from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import Page
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.services.activity import ActivityService
from app.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["Сотрудники"])


@router.get("", response_model=Page[EmployeeRead], summary="Список сотрудников")
def list_employees(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Page[EmployeeRead]:
    items, total = EmployeeService(db).list(limit, offset)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{employee_id}", response_model=EmployeeRead, summary="Получить сотрудника")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EmployeeRead:
    return EmployeeService(db).get_or_404(employee_id)


@router.post(
    "",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сотрудника (admin/manager)",
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> EmployeeRead:
    employee = EmployeeService(db).create(data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="create",
        entity="employee",
        entity_id=employee.id,
    )
    return employee


@router.patch(
    "/{employee_id}",
    response_model=EmployeeRead,
    summary="Обновить сотрудника (admin/manager)",
)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> EmployeeRead:
    employee = EmployeeService(db).update(employee_id, data)
    ActivityService(db).log(
        user_id=current_user.id,
        action="update",
        entity="employee",
        entity_id=employee_id,
    )
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить сотрудника (admin)",
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin)),
) -> None:
    EmployeeService(db).delete(employee_id)
    ActivityService(db).log(
        user_id=current_user.id,
        action="delete",
        entity="employee",
        entity_id=employee_id,
    )
