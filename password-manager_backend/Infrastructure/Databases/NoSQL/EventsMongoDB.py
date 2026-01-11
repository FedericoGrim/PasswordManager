from typing import Optional, List
from uuid import UUID
from Infrastructure.Databases.NoSQL.Models import UserEvent, EventPayload
from Domain.Interfaces.IEventsMongoDB import IEventsMongoDB


class EventRepository(IEventsMongoDB):
    def __init__(self, mongo_client: Optional[object] = None):
        # mongo_client is optional; Beanie is initialized at startup.
        self.mongo_client = mongo_client

    async def SaveEvent(self, EventType: str, Payload: dict):
        try:
            payload = EventPayload(**Payload)
            event = UserEvent(EventType=EventType, Payload=payload)
            await event.insert()
            return event
        except Exception:
            # Rilancia l'eccezione per essere gestita a livelli superiori
            raise

    async def GetEventsByUserId(self, UserId: UUID) -> List[UserEvent]:
        try:
            return await UserEvent.find(UserEvent.Payload.user_id == UserId).to_list()
        except Exception:
            raise

    async def GetAllEvents(self) -> List[UserEvent]:
        try:
            return await UserEvent.find_all().sort(-UserEvent.CreatedAt).to_list()
        except Exception:
            raise
