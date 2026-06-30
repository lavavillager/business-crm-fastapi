from enum import StrEnum


class UserRole(StrEnum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class AppointmentStatus(StrEnum):
    new = "new"
    confirmed = "confirmed"
    done = "done"
    cancelled = "cancelled"
