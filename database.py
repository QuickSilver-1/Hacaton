from gino import Gino
import sqlalchemy as sa
from typing import List
from aiogram import Dispatcher
from config import config_1
from sqlalchemy import Column, String, sql, ForeignKey, Integer

db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())

async def on_start(dispatcher: Dispatcher):
    await db.set_bind(config_1.POSTGRES_URL)

class Review(TimedBaseModel):
    __tablename__ = 'review'

    review_id = Column(Integer(), primary_key=True, autoincrement=True)
    tg_id = Column(ForeignKey('person.tg_id'))
    first_name = Column(String(50))
    last_name = Column(String(50))
    second_nam = Column(String(50))
    age = Column(String(10))
    city = Column(String(50))
    mark = Column(String(10))
    text = Column(String(1000))

    query: sql.select

class Person(TimedBaseModel):
    __tablename__ = 'person'
    __table_args__ = {'extend_existing': True}

    username_tg = Column(String(100))
    first_name = Column(String(50))
    last_name = Column(String(50))
    second_name = Column(String(50))
    email = Column(String(50))
    tg_id = Column(String(50), primary_key=True)
    number = Column(String(50))
    username = Column(String(50))
    password = Column(String(200))

    query: sql.select

class Admin(TimedBaseModel):
    __tablename__ = 'admin'

    username = Column(String(100))
    first_name = Column(String(50))
    last_name = Column(String(50))
    tg_id = Column(String(50), primary_key=True)

    query: sql.select

class Clinic(BaseModel):
    __tablename__ = 'clinic'

    region = Column(String(1000))
    link = Column(String(1000))
    number = Column(String(30))

    query: sql.select