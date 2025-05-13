from fastapi import APIRouter, HTTPException
from Domain.Objects.UserObj import UserCreate, UserUpdate
import uuid
from Application.UserInterface import InterfaceDeleteUser, InterfaceGetUser, InterfaceCreateUser, InterfaceUpdateUser

router = APIRouter()

@router.post("/")
async def CreateUser(user: UserCreate):
    createdUser = InterfaceCreateUser(user)
    if createdUser:
        return {"message": "User created successfully", "user": createdUser}
    else:
        raise HTTPException(status_code=400, detail="User creation failed")

@router.get("/")
async def GetUser(userEmail: str):
    user = InterfaceGetUser(userEmail)
    if user:
        return {"message": "User retrieved successfully", "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
async def UpdateUser(userId: uuid.UUID, userUpdated: UserUpdate):
    updatedUser = InterfaceUpdateUser(userId, userUpdated)
    if updatedUser:
        return {"message": "User updated successfully", "user": updatedUser}
    else:
        raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def DeleteUser(userId: uuid.UUID):
    if InterfaceDeleteUser(userId):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="User deletion failed")
