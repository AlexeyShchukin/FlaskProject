# Инспекция базы данных для автогенерации классов пайтона
# pip install sqlacodegen-v2
# sqlacodegen_v2 sqlite:///C:/python_projects/FlaskProject/database.db --outfile sqlalchemy_lessons/automap_db_inspect.py

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(120))
    description = mapped_column(Text)


class Users(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(25))
    age = mapped_column(Integer)
