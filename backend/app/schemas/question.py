from pydantic import BaseModel, Field

from app.models.enums import QuestionType


class QuestionCreate(BaseModel):
    poll_id: int
    text: str
    type: QuestionType
    order: int = Field(ge=1)
    options_json: str | None = None


class QuestionRead(BaseModel):
    id: int
    poll_id: int
    text: str
    type: str
    order: int
    options_json: str | None = None

    model_config = {"from_attributes": True}
