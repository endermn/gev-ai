from sqlalchemy import Column, Integer, String, DateTime, Text
from .base import Base
from datetime import datetime


class TerminalHistory(Base):
    __tablename__ = "terminal_history"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(Text, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    embedding = Column(Text, nullable=True)  # Store embedding as JSON string
