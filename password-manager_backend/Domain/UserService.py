from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
import uuid
from dotenv import load_dotenv

from Objects.UserObj import User, UserCreate, UserUpdate

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()

def CreateUser(dbSession, user: UserCreate):
    newUser = User(**user.dict())
    dbSession.add(newUser)
    dbSession.commit()
    dbSession.refresh(newUser)
    return newUser

def GetUser(dbSession, userEmail: str):
    return dbSession.query(User).filter(User.email == userEmail).first()

def UpdateUser(dbSession, userId: uuid.UUID, updatedUser: UserUpdate):
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
    return user

def DeleteUser(dbSession, userId: uuid.UUID):
    user = dbSession.query(User).filter(User.id == userId).first()
    if user:
        dbSession.delete(user)
        dbSession.commit()
    return user