from typing import Optional, List, Any
from uuid import UUID
from domain.events_payload.models import UserEvent, EventPayload
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB


class EventRepository(IEventsMongoDB):
    def __init__(self, mongo_client: Optional[object] = None):
        self.mongo_client = mongo_client

    async def save_event(self, event_type: str, user_id: UUID, changes: Optional[dict[str, Any]] = None):
        try:
            payload = EventPayload(
                user_id=user_id,
                action=event_type,
                changes=changes
            )
            event = UserEvent(event_type=event_type, payload=payload)
            await event.insert()

        except Exception:
            raise

    async def get_events_by_user_id(self, user_id: UUID) -> List[UserEvent]:
        try:
            return await UserEvent.find(UserEvent.payload.user_id == user_id).to_list()
        except Exception:
            raise

    async def get_all_events(self) -> List[UserEvent]:
        try:
            return await UserEvent.find_all().sort("-CreatedAt").to_list()
        except Exception:
            raise