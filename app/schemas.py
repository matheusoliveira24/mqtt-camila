from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    topic: str
    category: Optional[str]
    payload: Optional[Dict[str, Any]]
    raw: Optional[str]
    numeric_value: Optional[float]
    received_at: datetime

    class Config:
        orm_mode = True
