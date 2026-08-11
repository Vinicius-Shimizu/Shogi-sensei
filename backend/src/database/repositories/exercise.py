from src.database.models.exercise import Exercise
from src.database.repositories.base import BaseRepository
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from src.database.connection import engine
import random

USER_UNLOCKED_TYPES = {"checkmate-in-one": 1.0}

class ExerciseRepository(BaseRepository):
    model = Exercise

    def get_exercises_list(self):
        selected_types = random.choices(
            population=list(USER_UNLOCKED_TYPES.keys()),
            weights=list(USER_UNLOCKED_TYPES.values()),
            k=10,
        )
        query = (
            select(Exercise)
            .where(Exercise.type.in_(USER_UNLOCKED_TYPES.keys()))
            .order_by(func.random())
        )
        with Session(engine) as session:
            exercises = session.scalars(query).all()
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

