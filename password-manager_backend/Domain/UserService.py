from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os
import uuid
from dotenv import load_dotenv
import logging

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
        raise HTTPException(status_code=500, detail="Database connection error")
    
    finally:
        db.close()

def CreateUser(dbSession : Session, user: UserCreate):
    try:
        newUser = User(**user.dict())
        dbSession.add(newUser)
        dbSession.commit()
        dbSession.refresh(newUser)
        return newUser
    
    except IntegrityError:
        dbSession.rollback()
        raise HTTPException(status_code=400, detail="User already exists or violates DB constraints")
    
    except Exception as e:
        dbSession.rollback()
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="User creation failed")

def GetUser(dbSession : Session, userEmail: str):
    try:
        user = dbSession.query(User).filter(User.email == userEmail).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database error during user retrieval")

def UpdateUser(dbSession : Session, userId: uuid.UUID, updatedUser: UserUpdate):
    try:
        user = dbSession.query(User).filter(User.id == userId).first()
        if user:
            if updatedUser.username:
                user.username = updatedUser.username
                
            if updatedUser.email:
                user.email = updatedUser.email
                
            if updatedUser.password:
                user.password = updatedUser.password
                
            dbSession.commit()
            dbSession.refresh(user)
            
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")  
        
        return user
    
    except Exception as e:
        dbSession.rollback()
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="User update failed")

def DeleteUser(dbSession : Session, userId: uuid.UUID):
    try:
        user = dbSession.query(User).filter(User.id == userId).first()
        if user:
            dbSession.delete(user)
            dbSession.commit()
            
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    except Exception as e:
        dbSession.rollback()
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="User deletion failed")