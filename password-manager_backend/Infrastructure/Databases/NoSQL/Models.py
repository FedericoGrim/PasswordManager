from typing import Any, Dict, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from beanie import Document

class EventPayload(BaseModel):
    user_id: UUID
    # altri campi opzionali
    extra: Optional[Dict[str, Any]] = None

class UserEvent(Document):
    EventType: str
    Payload: EventPayload
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user_events"
        indexes = [
            "Payload.user_id",
            # eventualmente (EventType, CreatedAt) per query frequenti
        ]
