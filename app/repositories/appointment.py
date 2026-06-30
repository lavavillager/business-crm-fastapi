from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.core.enums import AppointmentStatus
from app.models.appointment import Appointment
from app.repositories.base import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    model = Appointment

    def get_with_relations(self, obj_id: int) -> Appointment | None:
        stmt = (
            select(Appointment)
            .where(Appointment.id == obj_id)
            .options(
                selectinload(Appointment.client),
                selectinload(Appointment.employee),
                selectinload(Appointment.service),
            )
        )
        return self.db.scalar(stmt)

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
    ) -> tuple[list[Appointment], int]:
        conditions = []
        if status is not None:
            conditions.append(Appointment.status == status)
        if date_from is not None:
            conditions.append(Appointment.scheduled_at >= date_from)
        if date_to is not None:
            conditions.append(Appointment.scheduled_at <= date_to)
        if client_id is not None:
            conditions.append(Appointment.client_id == client_id)
        if employee_id is not None:
            conditions.append(Appointment.employee_id == employee_id)

        stmt = select(Appointment)
        count_stmt = select(func.count()).select_from(Appointment)
        for cond in conditions:
            stmt = stmt.where(cond)
            count_stmt = count_stmt.where(cond)

        total = self.db.scalar(count_stmt) or 0
        stmt = (
            stmt.options(
                selectinload(Appointment.client),
                selectinload(Appointment.employee),
                selectinload(Appointment.service),
            )
            .order_by(Appointment.scheduled_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all()), total
