from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.service import Service
from app.repositories.service import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, db: Session) -> None:
        self.repo = ServiceRepository(db)

    def get_or_404(self, service_id: int) -> Service:
        service = self.repo.get(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Услуга не найдена"
            )
        return service

    def list(self, limit: int, offset: int):
        return self.repo.list(limit, offset), self.repo.count()

    def create(self, data: ServiceCreate) -> Service:
        service = Service(**data.model_dump())
        return self.repo.create(service)

    def update(self, service_id: int, data: ServiceUpdate) -> Service:
        service = self.get_or_404(service_id)
        return self.repo.update(service, data.model_dump(exclude_unset=True))

    def delete(self, service_id: int) -> None:
        service = self.get_or_404(service_id)
        self.repo.delete(service)
