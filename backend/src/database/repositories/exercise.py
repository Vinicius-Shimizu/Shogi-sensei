from src.database.models.exercise import Exercise
from src.database.repositories.base import BaseRepository
from sqlalchemy import select, func
import random


class ExerciseRepository(BaseRepository):
    model = Exercise

    def get_exercises_list(self, user_modules: dict):
        selected_types = random.choices(
            population=list(user_modules.keys()),
            weights=list(user_modules.values()),
            k=10,
        )
        query = (
            select(Exercise)
            .where(Exercise.type.in_(user_modules.keys()))
            .order_by(func.random())
        )
        exercises = self.session.scalars(query).all()
        exercises_by_type = {}

        for exercise in exercises:
            exercises_by_type.setdefault(exercise.type, []).append(exercise)

        # Seleciona os exercícios correspondentes aos tipos sorteados
        result = []

        for exercise_type in selected_types:
            available = exercises_by_type.get(exercise_type, [])

            if available:
                result.append(available.pop())

        return result

