from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, func, Integer
from sqlalchemy.dialects.postgresql import JSONB


from src.database.connection import Base

class ExerciseStatistics(Base):
    __tablename__ = "exercise_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.exercise_id"), nullable=False)
    module: Mapped[str] = mapped_column(String(50), nullable=False)
    pieces_used : Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    is_correct: Mapped[bool] = mapped_column(nullable=False)
    response_time_ms: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())