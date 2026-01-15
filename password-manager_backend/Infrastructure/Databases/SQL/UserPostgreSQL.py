from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.UserPostgreSQL_Exceptions import *

from Domain.Interfaces.IUserService import IUserService
from Domain.Entities.User import User

class UserService(IUserService):
    def __init__(self, db: Session):
        self.Db = db
        
    def CreateUser(self, new_user):
        try:
            with self.Db.begin():
                self.Db.add(new_user)
                self.Db.flush()
                self.Db.refresh(new_user)

            return new_user
        
        except IntegrityError:
            raise UserAlreadyExistsException()
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserCreationFailedException()
        
    def GetUserByKeycloakId(self, keycloak_user_id: uuid.UUID):
        try:
            user = self.Db.query(User).filter(User.id_keycloak == keycloak_user_id).first()
            if not user:
                raise GetAllUserByIdNotFoundException("No User found for the given Keycloak Id.")
            
            return user
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetAllUserByIdRetrivalException()
        
    def UpdateUserByUserId(self, UserId: uuid.UUID):
        try:
            with self.Db.begin():
                user = self.Db.query(User).filter(User.id == UserId).first()
                if not user:
                    raise UserNotFoundException("User not found.")
                
                self.Db.flush()
                self.Db.refresh(user)

            return user
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserUpdatePasswordException()
        
    def DeleteUserByUserId(self, userId: uuid.UUID):
        try:
            with self.Db.begin():
                user = self.Db.query(User).filter(User.id == userId).first()
                if not user:
                    raise UserNotFoundException("User not found.")

                self.Db.delete(user)
                
            return {"message": "User deleted successfully."}
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserDeleteException()