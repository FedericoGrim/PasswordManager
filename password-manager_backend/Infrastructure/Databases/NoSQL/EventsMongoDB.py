from typing import Optional, List, Any
from uuid import UUID
from Domain.EventsPayload.Models import UserEvent, EventPayload
from Domain.Interfaces.IEventsMongoDB import IEventsMongoDB


class EventRepository(IEventsMongoDB):
    def __init__(self, mongo_client: Optional[object] = None):
        self.mongo_client = mongo_client

    async def SaveEvent(self, EventType: str, user_id: UUID, changes: Optional[dict[str, Any]] = None):
        try:
            payload = EventPayload(
                user_id=user_id,
                action=EventType,
                changes=changes
            )
            event = UserEvent(EventType=EventType, Payload=payload)
            await event.insert()

        except Exception:
            raise

    async def GetEventsByUserId(self, UserId: UUID) -> List[UserEvent]:
        try:
            return await UserEvent.find(UserEvent.Payload.user_id == UserId).to_list()
        except Exception:
            raise

    async def GetAllEvents(self) -> List[UserEvent]:
        try:
            return await UserEvent.find_all().sort("-CreatedAt").to_list()
        except Exception:
            raise
