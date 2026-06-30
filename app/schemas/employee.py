from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    position: str = Field(min_length=1, max_length=255)
    specialization: str | None = None
    work_schedule: str | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = Field(default=None, min_length=1, max_length=255)
    specialization: str | None = None
    work_schedule: str | None = None


class EmployeeRead(EmployeeBase):
    id: int

    model_config = {"from_attributes": True}
