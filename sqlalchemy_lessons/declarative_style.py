# Declarative Style
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from sqlalchemy_lessons.connection import sqlite_engine, Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name = Column(String(25))
    age = Column(Integer)


Session = sessionmaker(bind=sqlite_engine)
session = Session()
print(session)

Base.metadata.create_all(bind=sqlite_engine)
user = User(
    name="Ivan",
    age=29
)
session.commit()
session.add(user)

session.close()
