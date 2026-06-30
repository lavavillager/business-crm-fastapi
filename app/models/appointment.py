from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AppointmentStatus
from app.db.base import Base, TimestampMixin


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[AppointmentStatus] = mapped_column(
        SAEnum(AppointmentStatus, name="appointment_status"),
        default=AppointmentStatus.new,
        index=True,
    )

    client: Mapped["Client"] = relationship(back_populates="appointments")  # noqa: F821
    employee: Mapped["Employee"] = relationship(  # noqa: F821
        back_populates="appointments"
    )
    service: Mapped["Service"] = relationship(  # noqa: F821
        back_populates="appointments"
    )
