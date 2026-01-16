import uuid

from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO
from Application.Exceptions.SubAccountUseCaseException import *

from Application.UseCase.Publisher import EventPublisher

class CreateSubAccountUseCase():
    """
    Use case for creating a subaccount.
    This class handles the creation of a subaccount by encrypting the password and interacting with the SubAccountRepository to persist the subaccount data.

    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
        salt (str): The salt used for hashing the password.
    """
    def __init__(self, SubAccountRepository, EventRepository=None):
        """
        Initializes the CreateSubAccountUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccount_create: CreateSubAccountDTO):
        """
        Executes the use case to create a subaccount.
        """
        try:
            result = self.SubAccountRepository.CreateSubAccount(subaccount_create)
            
            if self.EventRepository:
                EventPublisher.Publish(
                    EventType="SubAccountCreated",
                    Payload={
                        "subaccount_id": str(result.Id),
                        "user_id": str(subaccount_create.UserId)
                    }
                )
            
            return result
        except Exception as e:
            raise CreateSubAccountException(str(e)) from e
        
class GetAllSubAccountsByLocalUserIdUseCase():
    """
    Use case for retrieving all subaccounts associated with a user ID.
    This class interacts with the SubAccountRepository to fetch subaccounts based on the user ID.

    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
    """
    def __init__(self, SubAccountRepository):
        """
        Initializes the GetAllSubAccountsByLocalUserIdUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, userId: uuid.UUID):
        """
        Executes the use case to retrieve all subaccounts by user ID.
        """
        try:
            return self.SubAccountRepository.GetAllSubAccountsByUserId(userId)
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e
        
class UpdateSubAccountByIdUseCase():
    """
    Use case for updating a subaccount by ID.
    This class handles the update of a subaccount by interacting with the SubAccountRepository to persist the changes.
    
    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
        salt (str): The salt used for hashing the password.
    """
    def __init__(self, SubAccountRepository, EventRepository=None):
        """
        Initializes the UpdateSubAccountByIdUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccountId: uuid.UUID, new_subaccount: UpdateSubAccountDTO):
        """
        Executes the use case to update a subaccount by ID.
        """
        try:
            result = self.SubAccountRepository.UpdateSubAccountById(subaccountId, new_subaccount)
            
            if self.EventRepository:
                EventPublisher.Publish(
                    EventType="SubAccountUpdated",
                    Payload={
                        "subaccount_id": str(subaccountId)
                    }
                )
            
            return result
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e
        
class DeleteSubAccountByIdUseCase():
    """
    Use case for deleting a subaccount by ID.
    This class handles the deletion of a subaccount by interacting with the SubAccountRepository.
    
    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
    """
    def __init__(self, SubAccountRepository, EventRepository=None):
        """
        Initializes the DeleteSubAccountByIdUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccountId: uuid.UUID):
        """
        Executes the use case to delete a subaccount by ID.
        """
        try:
            result = self.SubAccountRepository.DeleteSubAccountById(subaccountId)
            
            if self.EventRepository:
                EventPublisher.Publish(
                    EventType="SubAccountDeleted",
                    Payload={
                        "subaccount_id": str(subaccountId)
                    }
                )
            
            return result
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e