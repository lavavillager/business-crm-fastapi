from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.client import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    def __init__(self, db: Session) -> None:
        self.repo = ClientRepository(db)

    def get_or_404(self, client_id: int) -> Client:
        client = self.repo.get(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
            )
        return client

    def search(self, query: str | None, limit: int, offset: int):
        return self.repo.search(query, limit, offset)

    def create(self, data: ClientCreate) -> Client:
        client = Client(**data.model_dump())
        return self.repo.create(client)

    def update(self, client_id: int, data: ClientUpdate) -> Client:
        client = self.get_or_404(client_id)
        return self.repo.update(client, data.model_dump(exclude_unset=True))

    def delete(self, client_id: int) -> None:
        client = self.get_or_404(client_id)
        self.repo.delete(client)
