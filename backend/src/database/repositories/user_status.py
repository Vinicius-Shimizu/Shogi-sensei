from src.database.models.user_status import UserStatus
from src.database.repositories.base import BaseRepository

class UserStatusRepository(BaseRepository):
    model = UserStatus
