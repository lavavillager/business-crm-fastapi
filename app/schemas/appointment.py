from datetime import datetime

from pydantic import BaseModel

from app.core.enums import AppointmentStatus
from app.schemas.client import ClientRead
from app.schemas.employee import EmployeeRead
from app.schemas.service import ServiceRead


class AppointmentBase(BaseModel):
    client_id: int
    employee_id: int
    service_id: int
    scheduled_at: datetime


class AppointmentCreate(AppointmentBase):
    status: AppointmentStatus = AppointmentStatus.new


class AppointmentUpdate(BaseModel):
    client_id: int | None = None
    employee_id: int | None = None
    service_id: int | None = None
    scheduled_at: datetime | None = None
    status: AppointmentStatus | None = None


class AppointmentRead(BaseModel):
    id: int
    scheduled_at: datetime
    status: AppointmentStatus
    client: ClientRead
    employee: EmployeeRead
    service: ServiceRead

    model_config = {"from_attributes": True}
