import uuid
from abc import ABC, abstractmethod

@abstractmethod
class IEventsMongoDB(ABC):
    @abstractmethod
    async def SaveEvent(self, EventType: str, Payload: dict):
        pass

    @abstractmethod
    async def GetEventsByUserId(self, UserId: uuid.UUID):
        pass

    @abstractmethod
    async def GetAllEvents(self):
        pass