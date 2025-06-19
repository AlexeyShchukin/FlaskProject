__all__ = (
    'engine',
    'Base'
)


from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# path_os = os.path.join(os.path.dirname(__file__), '.env.stage')
proj_path = Path(__file__).parent.parent
load_dotenv(proj_path / ".env.stage")

engine = create_engine(
    url=os.getenv("DB_URI"),
    echo=True
)

# engine = create_engine(
#     url=f"sqlite:///{proj_path}/database.db"
# )

Base = declarative_base()
