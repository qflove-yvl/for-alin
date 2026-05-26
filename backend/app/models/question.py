from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import QuestionType


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)
    type: Mapped[QuestionType] = mapped_column(String(32))
    order: Mapped[int] = mapped_column(Integer)
    options_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    poll = relationship("Poll", back_populates="questions")
