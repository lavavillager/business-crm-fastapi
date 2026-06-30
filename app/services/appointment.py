from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import AppointmentStatus
from app.models.appointment import Appointment
from app.repositories.appointment import AppointmentRepository
from app.repositories.client import ClientRepository
from app.repositories.employee import EmployeeRepository
from app.repositories.service import ServiceRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = AppointmentRepository(db)
        self.clients = ClientRepository(db)
        self.employees = EmployeeRepository(db)
        self.services = ServiceRepository(db)

    def _validate_refs(
        self, client_id: int, employee_id: int, service_id: int
    ) -> None:
        if not self.clients.get(client_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Клиент не найден")
        if not self.employees.get(employee_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Сотрудник не найден")
        if not self.services.get(service_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Услуга не найдена")

    def get_or_404(self, appointment_id: int) -> Appointment:
        appointment = self.repo.get_with_relations(appointment_id)
        if not appointment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Запись не найдена")
        return appointment

    def search(
        self,
        *,
        status: AppointmentStatus | None,
        date_from: datetime | None,
        date_to: datetime | None,
        client_id: int | None,
        employee_id: int | None,
        limit: int,
        offset: int,
    ):
        return self.repo.search(
            status=status,
            date_from=date_from,
            date_to=date_to,
            client_id=client_id,
            employee_id=employee_id,
            limit=limit,
            offset=offset,
        )

    def create(self, data: AppointmentCreate) -> Appointment:
        self._validate_refs(data.client_id, data.employee_id, data.service_id)
        appointment = Appointment(**data.model_dump())
        self.repo.create(appointment)
        return self.get_or_404(appointment.id)

    def update(self, appointment_id: int, data: AppointmentUpdate) -> Appointment:
        appointment = self.get_or_404(appointment_id)
        payload = data.model_dump(exclude_unset=True)
        self._validate_refs(
            payload.get("client_id", appointment.client_id),
            payload.get("employee_id", appointment.employee_id),
            payload.get("service_id", appointment.service_id),
        )
        self.repo.update(appointment, payload)
        return self.get_or_404(appointment_id)

    def delete(self, appointment_id: int) -> None:
        appointment = self.get_or_404(appointment_id)
        self.repo.delete(appointment)
