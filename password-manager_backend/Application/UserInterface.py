import uuid
from fastapi import Depends
from sqlalchemy.orm import Session

from Domain.UserService import get_db
from Domain.Objects.UserObj import UserCreate, UserUpdate
from Domain.IUserService import CreateUser, GetUser, UpdateUser, DeleteUser

def InterfaceCreateUser(user: UserCreate, db: Session = Depends(get_db)):
    return CreateUser(db, user)

def InterfaceGetUser(userEmail: str, db: Session = Depends(get_db)):
    return GetUser(db, userEmail)

def InterfaceUpdateUser(user_id: uuid.UUID, user: UserUpdate, db: Session = Depends(get_db)):
    return UpdateUser(db, user_id, user)

def InterfaceDeleteUser(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return DeleteUser(db, user_id)
