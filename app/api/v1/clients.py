from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.enums import UserRole
from app.db.session import get_db
from app.models.user import User
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.schemas.common import Page
from app.services.activity import ActivityService
from app.services.client import ClientService

router = APIRouter(prefix="/clients", tags=["Клиенты"])


@router.get("", response_model=Page[ClientRead], summary="Список / поиск клиентов")
def list_clients(
    q: str | None = Query(None, description="Поиск по имени, телефону или email"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Page[ClientRead]:
    items, total = ClientService(db).search(q, limit, offset)
    return Page(items=items, total=total, limit=limit, offset=offset)


@router.get("/{client_id}", response_model=ClientRead, summary="Получить клиента")
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ClientRead:
    return ClientService(db).get_or_404(client_id)


@router.post(
    "",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать клиента",
)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientRead:
    client = ClientService(db).create(data)
    ActivityService(db).log(
        user_id=current_user.id, action="create", entity="client", entity_id=client.id
    )
    return client


@router.patch("/{client_id}", response_model=ClientRead, summary="Обновить клиента")
def update_client(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientRead:
    client = ClientService(db).update(client_id, data)
    ActivityService(db).log(
        user_id=current_user.id, action="update", entity="client", entity_id=client_id
    )
    return client


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить клиента (admin/manager)",
)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
) -> None:
    ClientService(db).delete(client_id)
    ActivityService(db).log(
        user_id=current_user.id, action="delete", entity="client", entity_id=client_id
    )
