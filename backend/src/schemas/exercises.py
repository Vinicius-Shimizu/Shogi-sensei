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