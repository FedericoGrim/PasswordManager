from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import os
import uuid
from dotenv import load_dotenv
import logging

from Infrastructure.Exceptions.LocalUserPostgreSQL_Exceptions import *

from Domain.ILocalUserSercive import ILocalUserService
from Domain.Entities.LocalUser import LocalUser

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    except Exception as e:
        logging.error(f"Error: {e}")
        raise PostgreSqlConnectionException()
    
    finally:
        db.close()

class LocalUserService(ILocalUserService):
    def __init__(self, db: Session):
        self.Db = db
        
    def CreateLocalUser(self, localuser_create, generatedHash, generatedSalt):
        try:
            newLocalUser = localuser_create.to_entity(generatedHash, generatedSalt)
            self.Db.add(newLocalUser)
            self.Db.commit()
            self.Db.refresh(newLocalUser)
            return newLocalUser
            
        except IntegrityError:
            self.Db.rollback()
            raise LocalUserAlreadyExistsException()
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise LocalUserCreationFailedException()
        
    def GetAllLocalUserById(self, IdKeycloak: uuid.UUID):
        try:
            local_users = self.Db.query(LocalUser).filter(LocalUser.IdKeycloak == IdKeycloak).all()
            if not local_users:
                raise GetAllLocalUserByIdNotFoundException("No local users found for the given main user ID.")
            return local_users
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetAllLocalUserByIdRetrivalException()
        
    def UpdateLocalUserById(self, localUserId: uuid.UUID, new_hash: str):
        try:
            local_user = self.Db.query(LocalUser).filter(LocalUser.Id == localUserId).first()
            if not local_user:
                raise LocalUserNotFoundException("Local user not found.")
            
            local_user.HashMasterPassword = new_hash
            self.Db.commit()
            self.Db.refresh(local_user)
            return local_user
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise LocalUserUpdatePasswordException()
        
    def DeleteLocalUserById(self, userId: uuid.UUID):
        try:
            local_user = self.Db.query(LocalUser).filter(LocalUser.Id == userId).first()
            if not local_user:
                raise LocalUserNotFoundException("Local user not found.")
            
            self.Db.delete(local_user)
            self.Db.commit()
            return {"message": "Local user deleted successfully."}
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise LocalUserDeleteException()