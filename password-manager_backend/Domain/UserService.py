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

def CreateUser(db_session, user: UserCreate):
    newUser = User(**user.dict())
    db_session.add(newUser)
    db_session.commit()
    db_session.refresh(newUser)
    return newUser

def GetUser(db_session, userEmail: str):
    return db_session.query(User).filter(User.email == userEmail).first()

def UpdateUser(db_session, userId: uuid.UUID, updatedUser: UserUpdate):
    user = db_session.query(User).filter(User.id == userId).first()
    if user:
        if updatedUser.username:
            user.username = updatedUser.username
        if updatedUser.email:
            user.email = updatedUser.email
        if updatedUser.password:
            user.password = updatedUser.password
        db_session.commit()
        db_session.refresh(user)
    return user

def DeleteUser(db_session, userId: uuid.UUID):
    user = db_session.query(User).filter(User.id == userId).first()
    if user:
        db_session.delete(user)
        db_session.commit()
    return user