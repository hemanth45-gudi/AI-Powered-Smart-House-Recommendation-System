from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class InteractionBase(BaseModel):
    user_id: int
    house_id: Optional[int] = None
    event_type: str
    metadata_json: Optional[Dict[str, Any]] = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
