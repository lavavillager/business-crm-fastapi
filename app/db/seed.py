"""Загрузка демонстрационных данных (idempotent).

Запуск:
    python -m app.db.seed
Также вызывается автоматически при старте приложения, если SEED_ON_STARTUP=true.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums import AppointmentStatus, UserRole
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.employee import Employee
from app.models.service import Service
from app.models.user import User


def _seed_users(db: Session) -> None:
    if db.scalar(select(User).limit(1)):
        return
    users = [
        User(
            email=settings.FIRST_ADMIN_EMAIL,
            full_name="Главный администратор",
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            role=UserRole.admin,
        ),
        User(
            email="manager@crm.example.com",
            full_name="Мария Менеджер",
            hashed_password=hash_password("manager12345"),
            role=UserRole.manager,
        ),
        User(
            email="employee@crm.example.com",
            full_name="Иван Сотрудник",
            hashed_password=hash_password("employee12345"),
            role=UserRole.employee,
        ),
    ]
    db.add_all(users)
    db.commit()


def _seed_catalog(db: Session) -> None:
    if db.scalar(select(Client).limit(1)):
        return

    clients = [
        Client(name="Анна Смирнова", phone="+79001112233", email="anna@example.com",
               comment="Постоянный клиент"),
        Client(name="Пётр Иванов", phone="+79004445566", email="petr@example.com",
               comment="Предпочитает утренние записи"),
        Client(name="Ольга Кузнецова", phone="+79007778899", email=None,
               comment=None),
    ]
    employees = [
        Employee(name="Елена Парикмахер", position="Мастер", specialization="Стрижки",
                 work_schedule="Пн-Пт 09:00-18:00"),
        Employee(name="Дмитрий Барбер", position="Барбер", specialization="Бороды",
                 work_schedule="Вт-Сб 10:00-19:00"),
    ]
    services = [
        Service(name="Женская стрижка", price=Decimal("1500.00"),
                duration_minutes=60),
        Service(name="Мужская стрижка", price=Decimal("1000.00"),
                duration_minutes=45),
        Service(name="Оформление бороды", price=Decimal("700.00"),
                duration_minutes=30),
    ]
    db.add_all(clients + employees + services)
    db.commit()

    now = datetime.now(timezone.utc)
    appointments = [
        Appointment(client_id=clients[0].id, employee_id=employees[0].id,
                    service_id=services[0].id,
                    scheduled_at=now + timedelta(days=1, hours=2),
                    status=AppointmentStatus.confirmed),
        Appointment(client_id=clients[1].id, employee_id=employees[1].id,
                    service_id=services[1].id,
                    scheduled_at=now + timedelta(days=2, hours=1),
                    status=AppointmentStatus.new),
        Appointment(client_id=clients[2].id, employee_id=employees[0].id,
                    service_id=services[2].id,
                    scheduled_at=now - timedelta(days=1),
                    status=AppointmentStatus.done),
    ]
    db.add_all(appointments)
    db.commit()


def run_seed() -> None:
    db = SessionLocal()
    try:
        _seed_users(db)
        _seed_catalog(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
    print("Seed-данные успешно загружены.")
