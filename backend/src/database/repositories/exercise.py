from src.database.models.exercise import Exercise
from src.database.repositories.base import BaseRepository

class ExerciseRepository(BaseRepository):
    model = Exercise


