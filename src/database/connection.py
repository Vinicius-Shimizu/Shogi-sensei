import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://shogi_sensei:shogi@localhost:5433/shogi_sensei"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)


class Base(DeclarativeBase):
    pass