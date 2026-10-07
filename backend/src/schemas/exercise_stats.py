from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExerciseStat(BaseModel):
    user_id: int
    exercise_id: int
    module: str
    pieces_used: list[str]
    is_correct: bool
    response_time_ms: int

    model_config = ConfigDict(from_attributes=True)

class ExerciseStatList(ExerciseStat):
    exercises_stats: list[ExerciseStat]