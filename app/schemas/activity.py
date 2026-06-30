from datetime import datetime

from pydantic import BaseModel


class ActivityLogRead(BaseModel):
    id: int
    user_id: int | None
    action: str
    entity: str
    entity_id: int | None
    detail: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
