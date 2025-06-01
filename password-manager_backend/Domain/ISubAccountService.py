import uuid
from abc import ABC, abstractmethod

from Domain.Entities.SubAccount import SubAccount

@abstractmethod
class ISubAccountService(ABC):
    @abstractmethod
    def CreateSubAccount(self, subaccount: SubAccount) -> dict:
        pass

    @abstractmethod
    def GetAllSubAccountsByUserId(self, userId: uuid.UUID) -> dict:
        pass

    @abstractmethod
    def UpdateSubAccountById(self, subaccountId: uuid.UUID, new_subaccount: SubAccount) -> dict:
        pass

    @abstractmethod
    def DeleteSubAccountById(self, subaccountId: uuid.UUID) -> dict:
        pass