from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate, AnswerRead, PollResults
from app.services.analytics import build_poll_results

router = APIRouter(tags=["answers"])


@router.post("/answers/", response_model=AnswerRead)
def create_answer(payload: AnswerCreate, db: Session = Depends(get_db)):
    question = db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(status_code=400, detail="Question does not exist")

    answer = Answer(**payload.model_dump())
    db.add(answer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Answer already exists for this user/question")

    db.refresh(answer)
    return answer


@router.get("/polls/{poll_id}/results", response_model=PollResults)
def get_poll_results(poll_id: int, db: Session = Depends(get_db)):
    if not db.scalar(select(Question.id).where(Question.poll_id == poll_id)):
        raise HTTPException(status_code=404, detail="Poll or questions not found")
    return build_poll_results(db, poll_id)
