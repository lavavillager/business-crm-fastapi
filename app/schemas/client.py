from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ClientBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=3, max_length=32)
    email: EmailStr | None = None
    comment: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    phone: str | None = Field(default=None, min_length=3, max_length=32)
    email: EmailStr | None = None
    comment: str | None = None


class ClientRead(ClientBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
