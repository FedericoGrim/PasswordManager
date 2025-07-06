from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import os
import uuid
from dotenv import load_dotenv
import logging

from Infrastructure.Exceptions.SubAccountPostgreSQL_Exceptions import *

from Domain.ISubAccountService import ISubAccountService
from Domain.Entities.SubAccount import SubAccount

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    """
    Dependency that provides a database session.
    This function is used to create a new database session for each request.
    It yields a session object that can be used in the application.
    If an exception occurs, it logs the error and raises a custom exception.
    Finally, it ensures that the session is closed after use.

    Returns:
        Session: A SQLAlchemy session object for database operations.

    Raises:
        PostgreSqlConnectionException: If there is an error connecting to the PostgreSQL database.
    """
    db = SessionLocal()
    try:
        yield db
        
    except Exception as e:
        logging.error(f"Error: {e}")
        raise PostgreSqlConnectionException()
    
    finally:
        db.close()


class SubAccountService(ISubAccountService):
    def __init__(self, db: Session):
        """
        Initializes the LocalUserService with a database session.
        
        Args:
            db (Session): The database session to be used for operations.
        """
        self.Db = db

    def CreateSubAccount(self, subaccount):
        """        
        Creates a new subaccount in the database.

        Args:
            subaccount (SubAccount): The subaccount data to be created.

        Returns:
            SubAccount: The created subaccount entity.

        Raises:
            SubAccountAlreadyExistsException: If a subaccount with the same name already exists.
            SubAccountCreationFailedException: If the creation fails for any other reason.
        """
        try:
            subaccount_entity = SubAccount(
                user_id = subaccount.user_id,
                title = subaccount.title,
                username = subaccount.username,
                password_encrypted = subaccount.password_encrypted,
                url = subaccount.url
            )

            self.Db.add(subaccount_entity)
            self.Db.commit()
            self.Db.refresh(subaccount_entity)
            return subaccount_entity
            
        except IntegrityError:
            self.Db.rollback()
            raise SubAccountAlreadyExistsException("SubAccount with the same name already exists.")
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountCreationFailedException("Failed to create subaccount.")
        
    def GetAllSubAccountsByUserId(self, userId: uuid.UUID):
        """
        Retrieves all subaccounts associated with a given user ID.

        Args:
            userId (uuid.UUID): The ID of the user whose subaccounts are to be retrieved.

        Returns:
            list[SubAccount]: A list of subaccount entities associated with the user ID.

        Raises:
            GetAllSubAccountsByUserIdNotFoundException: If no subaccounts are found for the given user ID.
            SubAccountRetrievalException: If there is an error retrieving the subaccounts.
        """
        try:
            subaccounts: list[SubAccount] = self.Db.query(SubAccount).filter(SubAccount.user_id == userId).all()
            if not subaccounts:
                raise GetAllSubAccountsByUserIdNotFoundException("No subaccounts found for the given user ID.")
            return [subaccount for subaccount in subaccounts]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve subaccounts.")
        
    def UpdateSubAccountById(self, subaccountId: uuid.UUID, new_subaccount: SubAccount):
        """
        Updates an existing subaccount by its ID.

        Args:
            subaccountId (uuid.UUID): The ID of the subaccount to be updated.
            new_subaccount (SubAccount): The new subaccount data to be applied.

        Returns:
            SubAccount: The updated subaccount entity.

        Raises:
            SubAccountNotFoundException: If the subaccount with the given ID does not exist.
            SubAccountUpdateException: If there is an error updating the subaccount.
        """
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")
            
            for key, value in new_subaccount.to_dict().items():
                setattr(subaccount, key, value)
                
            self.Db.commit()
            return subaccount
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update subaccount.")
        
    def DeleteSubAccountById(self, subaccountId: uuid.UUID):
        """
        Deletes a subaccount by its ID.

        Args:
            subaccountId (uuid.UUID): The ID of the subaccount to be deleted.

        Returns:
            dict: A message indicating the success of the deletion.
            
        Raises:
            SubAccountNotFoundException: If the subaccount with the given ID does not exist.
            SubAccountDeletionException: If there is an error deleting the subaccount.
        """
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")
            
            self.Db.delete(subaccount)
            self.Db.commit()
            return {"message": "SubAccount deleted successfully."}
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountDeletionException("Failed to delete subaccount.")