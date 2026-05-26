from collections import defaultdict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.question import Question


def build_poll_results(db: Session, poll_id: int) -> dict:
    question_ids = db.scalars(select(Question.id).where(Question.poll_id == poll_id)).all()
    if not question_ids:
        return {"poll_id": poll_id, "participants": 0, "distributions": {}, "scale_means": {}}

    answers = db.execute(select(Answer).where(Answer.question_id.in_(question_ids))).scalars().all()
    participants = db.scalar(
        select(func.count(func.distinct(Answer.user_id))).where(Answer.question_id.in_(question_ids))
    ) or 0

    distributions = defaultdict(lambda: defaultdict(int))
    scale_values = defaultdict(list)

    q_map = {q.id: q for q in db.execute(select(Question).where(Question.id.in_(question_ids))).scalars().all()}

    for ans in answers:
        distributions[str(ans.question_id)][ans.answer] += 1
        q = q_map.get(ans.question_id)
        if q and q.type == "scale_1_5":
            try:
                scale_values[str(ans.question_id)].append(float(ans.answer))
            except ValueError:
                pass

    scale_means = {
        qid: (sum(values) / len(values) if values else None)
        for qid, values in scale_values.items()
    }

    return {
        "poll_id": poll_id,
        "participants": participants,
        "distributions": {qid: dict(v) for qid, v in distributions.items()},
        "scale_means": scale_means,
    }
