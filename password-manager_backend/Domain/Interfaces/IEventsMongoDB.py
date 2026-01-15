import uuid
from abc import ABC, abstractmethod

@abstractmethod
class IEventsMongoDB(ABC):
    @abstractmethod
    async def SaveEvent(self, EventType: str, Payload: dict):
        """
        Saves an event to the MongoDB database.

        Args:
            EventType (str): The type of the event (e.g., "UserCreated", "UserUpdated").
            Payload (dict): The payload data associated with the event.

        Returns:
            The saved event document.
        """
        pass

    @abstractmethod
    async def GetEventsByUserId(self, UserId: uuid.UUID):
        """
        Retrieves events associated with a given user ID.

        Args:
            UserId (uuid.UUID): The user ID to search for.

        Returns:
            A list of event documents associated with the user ID.
        """
        pass

    @abstractmethod
    async def GetAllEvents(self):
        """
        Retrieves all events from the MongoDB database.

        Returns:
            A list of all event documents.
        """
        pass