from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.UserPostgreSQL_Exceptions import *

from Domain.Interfaces.IUserService import IUserService
from Domain.Entities.User import User

class UserService(IUserService):
    def __init__(self, db: Session):
        self.db = db
        
    def create_user(self, new_user: User) -> User:
        try:
            self.db.add(new_user)
            self.db.flush()
            self.db.refresh(new_user)

            return new_user
        
        except IntegrityError:
            raise UserAlreadyExistsException()
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserCreationFailedException()
        
    def get_user_by_keycloak_id(self, keycloak_user_id: uuid.UUID):
        try:
            user = self.db.query(User).filter(User.id_keycloak == keycloak_user_id).first()            
            if not user:
                raise UserNotFoundException(f"User with keycloak_id {keycloak_user_id} not found.")
            return user
        
        except UserNotFoundException:
            raise
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetUserByIdRetrivalException()
        
    def update_user_by_id(self, user_id: uuid.UUID, new_user: User):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise UserNotFoundException("User not found.")
            
            for key, value in new_user.__dict__.items():
                if not key.startswith("_") and value is not None:
                    setattr(user, key, value)
            
            self.db.flush()
            self.db.refresh(user)

            return user
        
        except UserNotFoundException:
            raise
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserUpdateFailedException()
        
    def delete_user_by_id(self, user_id: uuid.UUID) -> dict[str, str]:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise UserNotFoundException("User not found.")

            self.db.delete(user)
                
            return {"message": "User deleted successfully."}
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserDeleteException()