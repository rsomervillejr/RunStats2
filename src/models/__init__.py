from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to register them with SQLAlchemy
from src.models.run_entry import RunEntry
from src.models.mile_split import MileSplit

__all__ = ['db', 'RunEntry', 'MileSplit']