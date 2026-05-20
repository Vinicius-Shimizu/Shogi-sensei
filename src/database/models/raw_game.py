from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB

from src.database.connection import Base


class RawGame(Base):
    __tablename__ = "raw_games"

    game_id: Mapped[str] = mapped_column(String, primary_key=True)
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

    

    

