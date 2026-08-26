from src.database.models.user import User
from src.database.repositories.base import BaseRepository
from sqlalchemy import update, select
from sqlalchemy.orm import Session
from src.database.connection import engine


class UserRepository(BaseRepository):
    model = User
