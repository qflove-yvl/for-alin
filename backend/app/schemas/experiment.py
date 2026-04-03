from pydantic import BaseModel


class VariantCreate(BaseModel):
    poll_id: int
    code: str
    title_override: str | None = None
    description_override: str | None = None
    weight: int = 1


class AssignmentRead(BaseModel):
    poll_id: int
    user_id: int
    variant_code: str
