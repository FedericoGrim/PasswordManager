import asyncio
from typing import Any
import uuid

from domain.interfaces.events_mongoDB_interface import IEventsMongoDB

class EventPublisher:
    def __init__(self, EventRepository: IEventsMongoDB):
        self.EventRepository = EventRepository

    def publish(self, event_type: str, payload: dict[Any, Any], user_id: uuid.UUID):
        asyncio.create_task(
            self._publishAsync(event_type, payload, user_id=user_id)
        )

    async def _publishAsync(self, event_type: str, payload: dict[str, Any], user_id: uuid.UUID) -> None:
        try:
            await self.EventRepository.save_event(event_type, changes=payload, user_id=user_id)
            
        except Exception:
            pass
