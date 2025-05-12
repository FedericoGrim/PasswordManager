from fastapi import APIRouter, HTTPException, Query
from Domain.Objects.UserObj import UserCreate, UserUpdate
import uuid

from Application.UserInterface import InterfaceDeleteUser, InterfaceGetUser, InterfaceCreateUser, InterfaceUpdateUser

router = APIRouter()

@router.post("/")
async def CreateUser(user: UserCreate):
    if InterfaceCreateUser(user):
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="User creation failed")

@router.get("/")
async def get_user(user_email: str = Query(..., description="Email of the user to retrieve")):
    user = InterfaceGetUser(user_email) 
    if user:
        return {"message": "User retrieved successfully", "user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
async def UpdateUser(user_id: uuid.UUID, user: UserUpdate):
    if InterfaceUpdateUser(user_id, user): 
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def DeleteUser(user_id: uuid.UUID):
    if InterfaceDeleteUser(user_id):  
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="User deletion failed")