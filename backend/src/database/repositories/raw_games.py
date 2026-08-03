from src.database.models.raw_game import RawGame
from src.database.repositories.base import BaseRepository
from sqlalchemy import update, select
from sqlalchemy.orm import Session
from src.database.connection import engine


class RawGameRepository(BaseRepository):
    model = RawGame

    def update_processed(self, ids: list[int]):
        with Session(engine) as session:
            session.execute(
                update(RawGame)
                .where(RawGame.game_id.in_(ids))
                .values(processed=True)
            )
            session.commit()

    def get_unprocessed_games(self, limit: int = 300):
        with Session(engine) as session:
            return session.scalars(
                select(RawGame)
                .where(RawGame.processed.is_(False))
                .order_by(RawGame.game_id)
                .limit(limit)
            ).all()