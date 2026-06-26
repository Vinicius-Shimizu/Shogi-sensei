from sqlalchemy import select, insert, func
from sqlalchemy.orm import Session
from src.database.connection import engine


class BaseRepository:
    model = None

    def __init__(self):
        if self.model is None:
            raise ValueError("Model não definida")

    def get_all(self):
        with Session(engine) as session:
            return session.scalars(
                select(self.model)
            ).all()

    def get_by_id(self, id_):
        with Session(engine) as session:
            return session.get(self.model, id_)

    def create(self, **kwargs):
        with Session(engine) as session:
            obj = self.model(**kwargs)

            session.add(obj)
            session.commit()
            session.refresh(obj)

            return obj

    def update(self, obj):
        with Session(engine) as session:
            session.merge(obj)
            session.commit()

    def delete(self, obj):
        with Session(engine) as session:
            session.delete(session.merge(obj))
            session.commit()
    
    def bulk_insert(self, rows: list[dict]):
        with Session(engine) as session:
            session.execute(
                insert(self.model),
                rows
            )
            session.commit()

    def get_random(self):
        with Session(engine) as session:
            return session.scalar(
                select(self.model)
                .order_by(func.random())
                .limit(1)
            )