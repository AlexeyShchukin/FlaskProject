# Classic Imperative Style
from sqlalchemy import Integer, String, Column, Text, Table
from sqlalchemy.orm import registry, sessionmaker

from sqlalchemy_lessons.connection import sqlite_engine

Register = registry()
news_table = Table(
    "news",
    Register.metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(120)),
    Column("description", Text)
)


class News:
    def __init__(self, title, description):
        self.title = title
        self.description = description


Session = sessionmaker(bind=sqlite_engine)
session = Session()
print(session)

Register.map_imperatively(News, news_table)
Register.metadata.create_all(sqlite_engine)

session.commit()
session.close()
