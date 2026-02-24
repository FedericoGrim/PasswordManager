import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Any

@abstractmethod
class IEventsMongoDB(ABC):
    @abstractmethod
    async def SaveEvent(self, EventType: str, user_id: uuid.UUID, changes: Optional[dict[str, Any]]):
        pass

    @abstractmethod
    async def GetEventsByUserId(self, UserId: uuid.UUID) -> List[Any]:
        pass

    @abstractmethod
    async def GetAllEvents(self) -> List[Any]:
        pass