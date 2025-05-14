from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os
import uuid
from dotenv import load_dotenv
import logging

from Infrastructure.Exceptions.UserPostgreSqlExcemption import *

from Domain.IUserService import IUserService
from Domain.Objects.UserObj import User, UserCreate, UserUpdate

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

class UserService(IUserService):
    def __init__(self, db):
        self.Db = db
        
    def CreateUser(self, user: UserCreate):
        try:
            newUser = User(**user.dict())
            self.Db.add(newUser)
            self.Db.commit()
            self.Db.refresh(newUser)
            return newUser
        
        except IntegrityError:
            self.Db.rollback()
            raise UserAlreadyExistsException()
        
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise UserCreationFailedException()

    def GetUser(self, userEmail: str):
        try:
            user = self.Db.query(User).filter(User.email == userEmail).first()
            if user is None:
                raise UserNotFoundException()
            
            return user
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise UserRetrievalException()

    def UpdateUser(self, userId: uuid.UUID, updatedUser: UserUpdate):
        try:
            user = self.Db.query(User).filter(User.id == userId).first()
            if user:
                if updatedUser.username:
                    user.username = updatedUser.username
                    
                if updatedUser.email:
                    user.email = updatedUser.email
                    
                if updatedUser.password:
                    user.password = updatedUser.password
                    
                self.Db.commit()
                self.Db.refresh(user)
                
            if user is None:
                raise UserNotFoundException()
            
            return user
        
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise UserUpdateException()

    def DeleteUser(self, userId: uuid.UUID):
        try:
            user = self.Db.query(User).filter(User.id == userId).first()
            if user:
                self.Db.delete(user)
                self.Db.commit()
                
            else:
                raise UserNotFoundException()
            
            return user
        
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise UserDeletionException()