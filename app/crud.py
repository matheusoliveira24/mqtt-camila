from sqlalchemy.orm import Session
from typing import Optional
from app import models

def create_message(db: Session, topic: str, payload: Optional[dict], raw: str, category: Optional[str], numeric_value: Optional[float]):
    m = models.Message(
        topic=topic,
        payload=payload,
        raw=raw,
        category=category,
        numeric_value=numeric_value
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def get_messages(db: Session, topic: Optional[str] = None, category: Optional[str] = None, limit: int = 100):
    q = db.query(models.Message)
    if topic:
        q = q.filter(models.Message.topic.like(f"%{topic}%"))
    if category:
        q = q.filter(models.Message.category == category)
    return q.order_by(models.Message.received_at.desc()).limit(limit).all()

def get_message_by_id(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

def get_latest(db: Session, limit: int = 100):
    return db.query(models.Message).order_by(models.Message.received_at.desc()).limit(limit).all()

