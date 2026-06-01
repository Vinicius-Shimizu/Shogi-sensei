from src.database.models.raw_game import RawGame
from src.database.repositories.base import BaseRepository

class RawGameRepository(BaseRepository):
    model = RawGame

