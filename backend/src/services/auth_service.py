from sqlalchemy.orm import Session
from src.database.repositories.user import UserRepository
from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash

class AuthenticationService():
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("JWT_ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.password_hash = PasswordHash.recommended()
        self.DUMMY_HASH = self.password_hash.hash("dummypassword")


    def check_password(self, plain_password: str, hashed_password: str):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_user(self, username: str):
        return self.user_repo.get_by_username(username)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            self.check_password(password, self.DUMMY_HASH)
            return False
        if not self.check_password(password, user.password):
            return False
        return user


    