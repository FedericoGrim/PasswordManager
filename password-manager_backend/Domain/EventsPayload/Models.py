from typing import Any, Dict, Optional
from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field
from beanie import Document


class EventPayload(BaseModel):
    user_id: UUID
    action: str  # es. "UserCreated", "PasswordUpdated", "UserDeleted"
    changes: Optional[Dict[str, Any]] = None  # es. {"salt": "nuovo_valore"}
    performed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserEvent(Document):
    EventType: str
    Payload: EventPayload
    CreatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "user_events"
        indexes = [
            "Payload.user_id",
            "Payload.performed_at",
        ]