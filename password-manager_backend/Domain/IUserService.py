import uuid

from sqlalchemy.orm import Session
from Domain.Objects.UserObj import UserCreate, UserUpdate
from Domain import UserService as UserServiceImpl

def CreateUser(db: Session, user: UserCreate):
    return UserServiceImpl.CreateUser(db, user)

def GetUser(db: Session, userEmail: str):
    return UserServiceImpl.GetUser(db, userEmail)

def UpdateUser(db: Session, user_id: uuid.UUID, user: UserUpdate):
    return UserServiceImpl.UpdateUser(db, user_id, user)

def DeleteUser(db: Session, user_id: uuid.UUID):
    return UserServiceImpl.DeleteUser(db, user_id)
