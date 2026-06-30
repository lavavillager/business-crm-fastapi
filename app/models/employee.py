from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    position: Mapped[str] = mapped_column(String(255))
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_schedule: Mapped[str | None] = mapped_column(String(255), nullable=True)

    appointments: Mapped[list["Appointment"]] = relationship(  # noqa: F821
        back_populates="employee"
    )
