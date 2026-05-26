from pydantic import BaseModel


class AnswerCreate(BaseModel):
    user_id: int
    question_id: int
    answer: str


class AnswerRead(BaseModel):
    id: int
    user_id: int
    question_id: int
    answer: str

    model_config = {"from_attributes": True}


class PollResults(BaseModel):
    poll_id: int
    participants: int
    distributions: dict
    scale_means: dict
