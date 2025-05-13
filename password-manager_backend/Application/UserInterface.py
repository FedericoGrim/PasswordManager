import uuid
from sqlalchemy.orm import Session

from Domain.Objects.UserObj import UserCreate, UserUpdate
from Infrastructure.IUserService import ICreateUser, IGetUser, IUpdateUser, IDeleteUser

def InterfaceCreateUser(user: UserCreate, db: Session):
    return ICreateUser(db, user)

def InterfaceGetUser(userEmail: str, db: Session):
    return IGetUser(db, userEmail)

def InterfaceUpdateUser(user_id: uuid.UUID, user: UserUpdate, db: Session):
    return IUpdateUser(db, user_id, user)

def InterfaceDeleteUser(user_id: uuid.UUID, db: Session):
    return IDeleteUser(db, user_id)
