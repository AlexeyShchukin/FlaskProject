__all__ = (
    'engine',
    'Base'
)


from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

proj_path = Path(__file__).parent.parent

engine = create_engine(
    url=f"sqlite:///{proj_path}/database.db"
)

Base = declarative_base()
