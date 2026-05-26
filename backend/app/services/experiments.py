import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment import ExperimentAssignment, ExperimentVariant


def assign_variant(db: Session, poll_id: int, user_id: int) -> ExperimentAssignment | None:
    existing = db.scalar(
        select(ExperimentAssignment).where(
            ExperimentAssignment.poll_id == poll_id,
            ExperimentAssignment.user_id == user_id,
        )
    )
    if existing:
        return existing

    variants = db.execute(select(ExperimentVariant).where(ExperimentVariant.poll_id == poll_id)).scalars().all()
    if not variants:
        return None

    weights = [max(v.weight, 1) for v in variants]
    picked = random.choices(variants, weights=weights, k=1)[0]

    assignment = ExperimentAssignment(user_id=user_id, poll_id=poll_id, variant_id=picked.id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
