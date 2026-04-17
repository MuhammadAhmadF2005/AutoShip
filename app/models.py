import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    code_snippet = Column(String(300))
    pylint_score = Column(Float)
    complexity_rating = Column(String)  # e.g., 'A', 'B', 'C', 'D', 'E', 'F'
    is_pass = Column(Boolean)
