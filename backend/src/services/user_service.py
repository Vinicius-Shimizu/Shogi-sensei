from sqlalchemy.orm import Session

from src.database.repositories.user import UserRepository
from src.database.repositories.user_status import UserStatusRepository


class UserService:

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.user_status_repo = UserStatusRepository(session)

    def create_user(self, username: str):
        existing_user = self.user_repo.get_by_username(username)

        if existing_user is not None:
            raise ValueError("Username already exists")
        try:
            user = self.user_repo.create(
                username=username
            )

            self.user_status_repo.create(
                user_id=user.id
            )

            self.session.commit()

            return user

        except Exception:
            self.session.rollback()
            raise