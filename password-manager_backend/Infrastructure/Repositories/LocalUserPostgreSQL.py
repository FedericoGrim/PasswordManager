from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.LocalUserPostgreSQL_Exceptions import *

from Domain.ILocalUserSercive import ILocalUserService
from Domain.Entities.LocalUser import LocalUser

class LocalUserService(ILocalUserService):
    def __init__(self, db: Session):
        """
        Initializes the LocalUserService with a database session.
        This constructor sets up the database session to be used for all operations related to local users.
        
        Args:
            db (Session): The database session to be used for operations.
        """
        self.Db = db
        
    def CreateLocalUser(self, localuser_create, generatedHash, generatedSalt):
        '''
        Creates a new local user in the database.

        Converts the `CreateLocalUser` DTO into a `LocalUser` entity using the provided hash and salt
        for the master password. Commits the new user to the database.

        If a user with the same Keycloak ID already exists, an exception is raised.
        Any unexpected errors during creation trigger a rollback and raise a generic exception.

        Args:
            localuser_create (CreateLocalUser): DTO containing user data.
            generatedHash (str): Hash of the master password.
            generatedSalt (str): Salt used to generate the hash.

        Returns:
            LocalUser: The newly created local user entity.

        Raises:
            LocalUserAlreadyExistsException: If a user with the same Keycloak ID already exists.
            LocalUserCreationFailedException: If an error occurs during user creation.
        '''
        try:
            with self.Db.begin():
                newLocalUser = localuser_create.to_entity(generatedHash, generatedSalt)
                self.Db.add(newLocalUser)
                self.Db.flush()
                self.Db.refresh(newLocalUser)
            return newLocalUser
        except IntegrityError:
            raise LocalUserAlreadyExistsException()
        except Exception as e:
            logging.error(f"Error: {e}")
            raise LocalUserCreationFailedException()

        
    def GetLocalUserById(self, IdKeycloak: uuid.UUID):
        '''        
        Retrieves a local users associated with a given Keycloak user ID.

        Args:
            IdKeycloak (uuid.UUID): The Keycloak user ID to search for.

        Returns:
            List[LocalUser]: A list of LocalUser entities associated with the given Keycloak user ID.

        Raises:
            GetAllLocalUserByIdNotFoundException: If no local users are found for the given Keycloak user ID.
            GetAllLocalUserByIdRetrivalException: If there is an error retrieving the local users.'''
        try:
            local_users = self.Db.query(LocalUser).filter(LocalUser.IdKeycloak == IdKeycloak).all()
            if not local_users:
                raise GetAllLocalUserByIdNotFoundException("No local users found for the given main user ID.")
            return local_users
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetAllLocalUserByIdRetrivalException()
        
    def UpdateLocalUserById(self, localUserId: uuid.UUID, new_hash: str):
        '''        
        Updates the master password hash of a local user by their ID.

        Args:
            localUserId (uuid.UUID): The ID of the local user to update.
            new_hash (str): The new hash for the master password.

        Returns:
            LocalUser: The updated local user entity.

        Raises:
            LocalUserNotFoundException: If the local user with the given ID does not exist.
            LocalUserUpdatePasswordException: If there is an error updating the local user.
        '''
        try:
            with self.Db.begin():
                local_user = self.Db.query(LocalUser).filter(LocalUser.Id == localUserId).first()
                if not local_user:
                    raise LocalUserNotFoundException("Local user not found.")
                
                local_user.HashMasterPassword = new_hash
                self.Db.refresh(local_user)
            return local_user
        except Exception as e:
            logging.error(f"Error: {e}")
            raise LocalUserUpdatePasswordException()
        
    def DeleteLocalUserById(self, userId: uuid.UUID):
        '''
        Deletes a local user by their ID.

        Args:
            userId (uuid.UUID): The ID of the local user to delete.

        Returns:
            dict: A message indicating the success of the deletion.

        Raises:
            LocalUserNotFoundException: If the local user with the given ID does not exist.
            LocalUserDeleteException: If there is an error deleting the local user.
        '''
        try:
            with self.Db.begin():
                local_user = self.Db.query(LocalUser).filter(LocalUser.Id == userId).first()
                if not local_user:
                    raise LocalUserNotFoundException("Local user not found.")
                
                self.Db.delete(local_user)
            return {"message": "Local user deleted successfully."}
        except Exception as e:
            logging.error(f"Error: {e}")
            raise LocalUserDeleteException()