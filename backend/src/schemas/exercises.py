from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExerciseResponse(BaseModel):
    exercise_id: int
    sfen: str
    hands: dict
    solution: str
    options: list[str]
    pieces_used: list[str]
    type: str

    model_config = ConfigDict(from_attributes=True)

class ExerciseAnswer(BaseModel):
    exercise_id: int
    answer: str

class ExerciseListSubmission(BaseModel):
    user_id: int
    answers: list[ExerciseAnswer]

class ExerciseResult(BaseModel):
    exercise_id: int
    exercise_type: str
    answer: str
    solution: str
    is_correct: bool

class ExerciseListResult(BaseModel):
    user_id: int
    score: float
    results: list[ExerciseResult]