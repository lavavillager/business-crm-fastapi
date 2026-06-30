from decimal import Decimal

from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    duration_minutes: int = Field(gt=0)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    duration_minutes: int | None = Field(default=None, gt=0)


class ServiceRead(ServiceBase):
    id: int

    model_config = {"from_attributes": True}
