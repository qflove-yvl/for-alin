from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExperimentVariant(Base):
    __tablename__ = "experiment_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(32))
    title_override: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_override: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    weight: Mapped[int] = mapped_column(Integer, default=1)


class ExperimentAssignment(Base):
    __tablename__ = "experiment_assignments"
    __table_args__ = (
        Index("ux_assignment_user_poll", "user_id", "poll_id", unique=True),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"), index=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("experiment_variants.id", ondelete="CASCADE"), index=True)
