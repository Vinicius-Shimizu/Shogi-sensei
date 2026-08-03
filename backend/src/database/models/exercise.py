from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB

from src.database.connection import Base


class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sfen: Mapped[str] = mapped_column(String, nullable=False)
    hands: Mapped[dict[dict]] = mapped_column(JSONB, nullable=False)
    solution: Mapped[str] = mapped_column(String, nullable=False)
    options: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    pieces_used: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)