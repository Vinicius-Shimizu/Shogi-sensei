from src.database.models.user_status import UserStatus
from src.database.repositories.base import BaseRepository
from sqlalchemy import update, select
from sqlalchemy.orm import Session
from src.database.connection import engine


class UserStatusRepository(BaseRepository):
    model = UserStatus
