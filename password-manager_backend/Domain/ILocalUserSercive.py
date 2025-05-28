import uuid
from abc import ABC, abstractmethod

from Domain.Entities.LocalUser import LocalUser

@abstractmethod
class ILocalUserService(ABC):
    @abstractmethod
    def CreateLocalUser(self, user: LocalUser, hash, salt) -> dict:
        pass

    @abstractmethod
    def GetAllLocalUserById(self, MainUserId: str) -> dict:
        pass

    @abstractmethod
    def UpdateLocalUserById(self, userId: uuid.UUID, newLocalUser: str) -> dict:
        pass

    @abstractmethod
    def DeleteLocalUserById(self, userId: uuid.UUID) -> dict:
        pass