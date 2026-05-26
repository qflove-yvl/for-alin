from datetime import datetime

from pydantic import BaseModel


class PollCreate(BaseModel):
    title: str
    description: str | None = None
    owner_id: int
    is_active: bool = True


class PollRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
