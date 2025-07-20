import uuid

from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO
from Application.Exceptions.SubAccountUseCaseException import *

from Domain.PasswordCripting import PasswordCripting

class CreateSubAccountUseCase():
    """
    Use case for creating a subaccount.
    This class handles the creation of a subaccount by encrypting the password and interacting with the SubAccountRepository to persist the subaccount data.

    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
        salt (str): The salt used for hashing the password.
    """
    def __init__(self, SubAccountRepository):
        """
        Initializes the CreateSubAccountUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccount_create: CreateSubAccountDTO, salt = str):
        """
        Executes the use case to create a subaccount.
        """
        try:
            subaccount_create.password_encrypted = PasswordCripting.hashPassword(subaccount_create.password_encrypted, salt)
            return self.SubAccountRepository.CreateSubAccount(subaccount_create)
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
    def __init__(self, SubAccountRepository):
        """
        Initializes the UpdateSubAccountByIdUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccountId: uuid.UUID, new_subaccount: UpdateSubAccountDTO, salt = str):
        """
        Executes the use case to update a subaccount by ID.
        """
        try:
            return self.SubAccountRepository.UpdateSubAccountById(subaccountId, new_subaccount)
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e
        
class DeleteSubAccountByIdUseCase():
    """
    Use case for deleting a subaccount by ID.
    This class handles the deletion of a subaccount by interacting with the SubAccountRepository.
    
    Attributes:
        SubAccountRepository (ISubAccountService): The repository interface for subaccount operations.
    """
    def __init__(self, SubAccountRepository):
        """
        Initializes the DeleteSubAccountByIdUseCase with a SubAccountRepository.
        """
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccountId: uuid.UUID):
        """
        Executes the use case to delete a subaccount by ID.
        """
        try:
            return self.SubAccountRepository.DeleteSubAccountById(subaccountId)
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e