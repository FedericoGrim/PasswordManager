import uuid
from abc import ABC, abstractmethod

from Domain.Entities.SubAccount import SubAccount

@abstractmethod
class ISubAccountService(ABC):
    @abstractmethod
    def CreateSubAccount(self, subaccount: SubAccount) -> dict:
        """
        Creates a new subaccount in the database.

        Args:
            subaccount (SubAccount): The subaccount data to be created.
            
        Returns:
            dict: The created subaccount entity.
        """
        pass

    @abstractmethod
    def GetAllSubAccountsByUserId(self, userId: uuid.UUID) -> dict:
        """
        Retrieves all subaccounts associated with a specific user ID.

        Args:
            userId (uuid.UUID): The ID of the user whose subaccounts are to be retrieved.

        Returns:
            dict: A list of subaccounts associated with the user ID.
        """
        pass

    @abstractmethod
    def UpdateSubAccountById(self, subaccountId: uuid.UUID, new_subaccount: SubAccount) -> dict:
        """
        Updates an existing subaccount by its ID.

        Args:
            subaccountId (uuid.UUID): The ID of the subaccount to be updated.
            new_subaccount (SubAccount): The new subaccount data to replace the existing one.

        Returns:
            dict: The updated subaccount entity.
        """
        pass

    @abstractmethod
    def DeleteSubAccountById(self, subaccountId: uuid.UUID) -> dict:
        """
        Deletes a subaccount by its ID.

        Args:
            subaccountId (uuid.UUID): The ID of the subaccount to be deleted.

        Returns:
            dict: The result of the deletion operation.
        """
        pass