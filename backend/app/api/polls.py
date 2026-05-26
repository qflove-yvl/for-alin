from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.poll import Poll
from app.models.user import User
from app.schemas.poll import PollCreate, PollRead

router = APIRouter(tags=["polls"])


@router.post("/polls/", response_model=PollRead)
def create_poll(payload: PollCreate, db: Session = Depends(get_db)):
    owner = db.get(User, payload.owner_id)
    if not owner:
        raise HTTPException(status_code=400, detail="Owner does not exist")

    poll = Poll(**payload.model_dump())
    db.add(poll)
    db.commit()
    db.refresh(poll)
    return poll


@router.get("/polls/{poll_id}", response_model=PollRead)
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll


@router.get("/polls/user/{user_id}", response_model=list[PollRead])
def get_user_polls(user_id: int, db: Session = Depends(get_db)):
    polls = db.execute(select(Poll).where(Poll.owner_id == user_id).order_by(Poll.created_at.desc())).scalars().all()
    return polls


@router.delete("/polls/{poll_id}")
def delete_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = db.get(Poll, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    db.delete(poll)
    db.commit()
    return {"status": "deleted"}
