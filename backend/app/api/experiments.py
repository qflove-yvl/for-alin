from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.experiment import ExperimentVariant
from app.schemas.experiment import AssignmentRead, VariantCreate
from app.services.experiments import assign_variant

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/variants")
def create_variant(payload: VariantCreate, db: Session = Depends(get_db)):
    variant = ExperimentVariant(**payload.model_dump())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return {"id": variant.id, "code": variant.code}


@router.post("/{poll_id}/assign/{user_id}", response_model=AssignmentRead)
def assign_user(poll_id: int, user_id: int, db: Session = Depends(get_db)):
    assignment = assign_variant(db, poll_id=poll_id, user_id=user_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="No variants configured for poll")

    variant = db.scalar(select(ExperimentVariant).where(ExperimentVariant.id == assignment.variant_id))
    return AssignmentRead(poll_id=poll_id, user_id=user_id, variant_code=variant.code)
