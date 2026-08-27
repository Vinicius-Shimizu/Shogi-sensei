from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config=ConfigDict(from_attributes=True)

class UserStatusResponse(BaseModel):
    user_id: int
    current_module: str
    module_progress: float
    modules_probs: dict
    recent_performances: list
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)