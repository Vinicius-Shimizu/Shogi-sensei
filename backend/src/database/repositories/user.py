from src.database.models.user import User
from src.database.repositories.base import BaseRepository
from sqlalchemy import select

class UserRepository(BaseRepository):
    model = User

    def get_by_username(self, username: str):
        return self.session.scalar(
            select(User).where(User.username == username)
        )