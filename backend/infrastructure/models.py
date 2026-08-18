# backend/infrastructure/models.py
import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    rules_triggered = Column(Integer, default=0)
    explanation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<AnalysisLog(id={self.id}, url='{self.url[:30]}...', risk_level='{self.risk_level}')>"
