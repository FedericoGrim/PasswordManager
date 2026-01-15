import asyncio

class EventPublisher:
    def __init__(self, EventRepository):
        self.EventRepository = EventRepository

    def Publish(self, EventType: str, Payload: dict):
        asyncio.create_task(
            self._PublishAsync(EventType, Payload)
        )

    async def _PublishAsync(self, EventType: str, Payload: dict):
        try:
            await self.EventRepository.SaveEvent(EventType, Payload)
        except Exception:
            # LOG
            pass
