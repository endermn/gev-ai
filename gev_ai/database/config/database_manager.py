from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class DatabaseManager:
    engine: Engine

    def __init__(self):
        self.engine = create_engine("sqlite:///gev-ai.db")

database_manager = DatabaseManager()
