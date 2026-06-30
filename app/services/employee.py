from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repo = EmployeeRepository(db)

    def get_or_404(self, employee_id: int) -> Employee:
        employee = self.repo.get(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Сотрудник не найден"
            )
        return employee

    def list(self, limit: int, offset: int):
        return self.repo.list(limit, offset), self.repo.count()

    def create(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.model_dump())
        return self.repo.create(employee)

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get_or_404(employee_id)
        return self.repo.update(employee, data.model_dump(exclude_unset=True))

    def delete(self, employee_id: int) -> None:
        employee = self.get_or_404(employee_id)
        self.repo.delete(employee)
