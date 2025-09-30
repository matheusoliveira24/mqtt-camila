from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import crud
from app.schemas import MessageOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[MessageOut], summary="Listar mensagens")
def list_messages(topic: Optional[str] = Query(None, description="Filtrar por parte do tópico"),
                  category: Optional[str] = Query(None, description="Filtrar por categoria"),
                  limit: int = Query(100, ge=1, le=1000, description="Número máximo de mensagens"),
                  db: Session = Depends(get_db)):
    return crud.get_messages(db, topic=topic, category=category, limit=limit)

@router.get("/latest", response_model=List[MessageOut], summary="Últimas mensagens")
def latest(limit: int = Query(50, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.get_latest(db, limit=limit)

@router.get("/{message_id}", response_model=MessageOut, summary="Obter mensagem por id")
def get_message(message_id: int, db: Session = Depends(get_db)):
    m = crud.get_message_by_id(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return m
