import asyncio
from typing import Any
import uuid

from Domain.Interfaces.IEventsMongoDB import IEventsMongoDB

class EventPublisher:
    def __init__(self, EventRepository: IEventsMongoDB):
        self.EventRepository = EventRepository

    def Publish(self, EventType: str, Payload: dict[Any, Any], user_id: uuid.UUID):
        asyncio.create_task(
            self._PublishAsync(EventType, Payload, user_id=user_id)
        )

    async def _PublishAsync(self, EventType: str, Payload: dict[str, Any], user_id: uuid.UUID) -> None:
        try:
            await self.EventRepository.SaveEvent(EventType, changes=Payload, user_id=user_id)
            
        except Exception:
            pass
