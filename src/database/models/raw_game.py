from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database.connection import Base


class RawGame(Base):
    __tablename__ = "raw_games"

    game_id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    names: Mapped[str] = mapped_column(
        String,
        nullable=False
    )