import uuid

from Application.DTO.V2.LocalUserDTO import CreateLocalUserDTOV2, UpdateLocalUserDTOV2
from Domain.PasswordCripting.PasswordCripting import *
from Application.Exceptions.LocalUserUseCaseExceptions import *

class CreateLocalUserUseCase():
    """
    Use case for creating a local user.
    It interacts with the LocalUserRepository to persist the user data.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the CreateLocalUserUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localuser_create: CreateLocalUserDTOV2):
        """
        Executes the use case to create a local user.
        """
        try:
            return self.LocalUserRepository.CreateLocalUser(localuser_create, localuser_create.Salt)
        except Exception as e:
            raise LocalUserCreationException(str(e)) from e

class GetLocalUsersByMainUserIdUseCase():
    """
    Use case for retrieving a local users associated with a main user ID.
    This class interacts with the LocalUserRepository to fetch local users based on the main user ID.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the GetAllLocalUsersByMainUserIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, mainUserId: uuid.UUID):
        """
        Executes the use case to retrieve all local users by main user ID.
        """
        try:
            return self.LocalUserRepository.GetLocalUserById(mainUserId)
        except Exception as e:
            raise LocalUserRetrievalException(str(e)) from e
        
class UpdateLocalUserByIdUseCase():
    """
    Use case for updating a local user by ID.
    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the UpdateLocalUserByIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, localUserId: uuid.UUID, new_local_user: UpdateLocalUserDTOV2, salt: bytes):
        """
        Executes the use case to update a local user by ID.
        """
        try:
            newCriptedPassword = CriptPassword(new_local_user.NewMasterPassword, new_local_user.NewMasterPassword, salt)
            return self.LocalUserRepository.UpdateLocalUserById(localUserId, newCriptedPassword)
        except Exception as e:
            raise LocalUserUpdateException(str(e)) from e        

class DeleteLocalUserByIdUseCase():
    """ 
    Use case for deleting a local user by ID.
    This class handles the deletion of a local user by interacting with the LocalUserRepository.

    Attributes:
        LocalUserRepository (ILocalUserService): The repository interface for local user operations.
    """
    def __init__(self, LocalUserRepository):
        """
        Initializes the DeleteLocalUserByIdUseCase with a LocalUserRepository.
        """
        self.LocalUserRepository = LocalUserRepository
        
    def execute(self, user_id: uuid.UUID):
        """
        Executes the use case to delete a local user by ID.
        """
        try:
            return self.LocalUserRepository.DeleteLocalUserById(user_id)
        except Exception as e:
            raise LocalUserDeletionException(str(e)) from e