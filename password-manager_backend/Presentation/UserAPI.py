from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid

from Domain.Objects.UserObj import UserCreate, UserUpdate
from Domain.UserService import get_db
from Application.UserInterface import InterfaceDeleteUser, InterfaceGetUser, InterfaceCreateUser, InterfaceUpdateUser

router = APIRouter()

@router.post("/")
async def ApiCreateUser(user: UserCreate, db: Session = Depends(get_db)):
    print(f"User type: {type(user)}") 
    createdUser = InterfaceCreateUser(user, db)
    if createdUser:
        return {"message": "User created successfully", "user": createdUser}
    else:
        raise HTTPException(status_code=400, detail="User creation failed")

@router.get("/")
async def ApiGetUser(userEmail: str, db: Session = Depends(get_db)):
    user = InterfaceGetUser(userEmail, db)
    if user:
        return {"message": "User retrieved successfully", "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
async def ApiUpdateUser(userId: uuid.UUID, userUpdated: UserUpdate, db: Session = Depends(get_db)):
    userUpdated = InterfaceUpdateUser(userId, userUpdated, db)
    if userUpdated:
        return {"message": "User updated successfully", "user": userUpdated}
    else:
        raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def ApiDeleteUser(userId: uuid.UUID, db: Session = Depends(get_db)):
    if InterfaceDeleteUser(userId, db):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="User deletion failed")
