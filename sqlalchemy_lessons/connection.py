import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

engine = create_engine(
    url=""
)

print(engine)
print(__file__)  # путь к файлу
print(Path(__file__).parent)  # путь к папке sqlalchemy_lessons
print(Path(__file__).parent.parent)  # путь к проекту

proj_path = Path(__file__).parent.parent
Base = declarative_base()
sqlite_engine = create_engine(
    url=f"sqlite:///{proj_path}/database.db"
)

print(sqlite_engine)
