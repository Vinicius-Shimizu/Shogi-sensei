from src.database.models.raw_game import RawGame
from src.database.repositories.base import BaseRepository
from sqlalchemy import update, select


class RawGameRepository(BaseRepository):
    model = RawGame

    def update_processed(self, ids: list[int]):
        self.session.execute(
            update(RawGame)
            .where(RawGame.game_id.in_(ids))
            .values(processed=True)
        )

    def get_unprocessed_games(self, limit: int = 300):
        return self.session.scalars(
            select(RawGame)
            .where(RawGame.processed.is_(False))
            .order_by(RawGame.game_id)
            .limit(limit)
        ).all()