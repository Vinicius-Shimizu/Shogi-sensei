from src.database.models.exercise_statistics import ExerciseStatistics
from src.database.repositories.base import BaseRepository


class ExerciseStatisticsRepository(BaseRepository):
    model = ExerciseStatistics