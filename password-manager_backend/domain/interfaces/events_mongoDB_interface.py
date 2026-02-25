import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Any

@abstractmethod
class IEventsMongoDB(ABC):
    @abstractmethod
    async def save_event(self, event_type: str, user_id: uuid.UUID, changes: Optional[dict[str, Any]]):
        pass

    @abstractmethod
    async def get_events_by_user_id(self, user_id: uuid.UUID) -> List[Any]:
        pass

    @abstractmethod
    async def get_all_events(self) -> List[Any]:
        pass