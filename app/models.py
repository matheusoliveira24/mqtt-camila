from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy import JSON as SA_JSON
from sqlalchemy.sql import func
from app.db import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), index=True, nullable=False)
    category = Column(String(80), index=True, nullable=True)
    payload = Column(SA_JSON, nullable=True)  # JSON if available (MySQL 5.7+), else SQLAlchemy handles it
    raw = Column(Text, nullable=True)
    numeric_value = Column(Float, nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
