import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD") 
DB_NAME = os.getenv("POSTGRES_DB") 
DB_IP = os.getenv("POSTGRES_IP")
DB_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


class Base(DeclarativeBase):
    pass