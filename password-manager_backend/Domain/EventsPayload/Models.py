from typing import Any, Dict, Optional
from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field
from beanie import Document


class EventPayload(BaseModel):
    user_id: UUID
    action: str
    changes: Optional[Dict[str, Any]] = None
    performed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserEvent(Document):
    event_type: str
    payload: EventPayload
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "user_events"
        indexes = [
            "payload.user_id",
            "payload.performed_at",
        ]