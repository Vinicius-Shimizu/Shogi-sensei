from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from src.database.connection import Base


class RawGame(Base):
    __tablename__ = "raw_games"

    game_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_comment: Mapped[str | None] = mapped_column(String, nullable=True)
    endgame: Mapped[str] = mapped_column(String, nullable=False)
    sfen: Mapped[str] = mapped_column(String, nullable=False)
    win: Mapped[int] = mapped_column(Integer, nullable=False)
    moves: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    players: Mapped[dict] = mapped_column(JSONB, nullable=False)
    moves_comments: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    ratings: Mapped[list[int]] = mapped_column(JSONB, nullable=False)
    scores: Mapped[list[int]] = mapped_column(JSONB, nullable=False)
    times: Mapped[list[int]] = mapped_column(JSONB, nullable=False)
    var_info: Mapped[dict] = mapped_column(JSONB, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    

    

