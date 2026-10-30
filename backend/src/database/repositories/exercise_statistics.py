from src.database.models.exercise_statistics import ExerciseStatistics
from src.database.repositories.base import BaseRepository


class ExerciseStatisticsRepository(BaseRepository):
    model = ExerciseStatistics

    def get_all_paginated(self, limit: int, offset: int):
        stats = (
            self.session.query(ExerciseStatistics)
            .order_by(ExerciseStatistics.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

        total = self.session.query(ExerciseStatistics).count()

        return {
            "data": stats,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + len(stats) < total
        }