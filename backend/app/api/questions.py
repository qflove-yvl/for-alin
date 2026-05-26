from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.poll import Poll
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionRead

router = APIRouter(tags=["questions"])


@router.post("/questions/", response_model=QuestionRead)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    poll = db.get(Poll, payload.poll_id)
    if not poll:
        raise HTTPException(status_code=400, detail="Poll does not exist")

    data = payload.model_dump(exclude={"type"})
    question = Question(**data, type=payload.type.value)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get("/polls/{poll_id}/questions", response_model=list[QuestionRead])
def get_poll_questions(poll_id: int, db: Session = Depends(get_db)):
    rows = db.execute(select(Question).where(Question.poll_id == poll_id).order_by(Question.order.asc())).scalars().all()
    return rows
