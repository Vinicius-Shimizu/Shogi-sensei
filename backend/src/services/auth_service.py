from sqlalchemy.orm import Session
from src.services.user_service import UserService
from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
import jwt
from src.auth.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthenticationService():
    def __init__(self, session: Session):
        self.session = session

        self.password_hash = PasswordHash.recommended()
        self.DUMMY_HASH = self.password_hash.hash("dummypassword")


    def check_password(self, plain_password: str, hashed_password: str):
        return self.password_hash.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user_service = UserService(self.session)
        user = user_service.get_user_by_username(username)
        if not user:
            self.check_password(password, self.DUMMY_HASH)
            return False
        if not self.check_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt



    