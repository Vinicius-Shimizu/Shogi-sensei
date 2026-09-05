from sqlalchemy import select, insert, func
from sqlalchemy.orm import Session
from src.database.connection import engine


class BaseRepository:
    model = None

    def __init__(self, session: Session):
        if self.model is None:
            raise ValueError("Model não definida")
        self.session = session

    def get_all(self):
        return self.session.scalars(
            select(self.model)
        ).all()

    def get_by_id(self, id_):
        return self.session.get(self.model, id_)

    def create(self, **kwargs):
        obj = self.model(**kwargs)

        self.session.add(obj)
        self.session.flush()

        return obj

    def update(self, obj):
        return self.session.merge(obj)

    def delete(self, obj):
        self.session.delete(obj)
    
    def bulk_insert(self, rows: list[dict]):
        self.session.execute(
            insert(self.model),
            rows
        )

    def get_random(self, limit=1):
        return self.session.scalars(
            select(self.model)
            .order_by(func.random())
            .limit(limit)
        ).all()