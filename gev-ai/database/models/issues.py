from .base import Base
from sqlalchemy import Column, Integer, String

class Issues(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    issue_description = Column(String, nullable=False)
