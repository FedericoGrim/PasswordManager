from fastapi import APIRouter, HTTPException, Query
from Domain.Objects.UserObj import UserCreate, UserUpdate
from sqlalchemy import Uuid

from Application.UserInterface import InterfaceDeleteUser, InterfaceGetUser, InterfaceCreateUser, InterfaceUpdateUser

router = APIRouter()

@router.post("/")
async def create_user(user: UserCreate):
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
async def update_user(user_id: Uuid, user: UserUpdate):
    if InterfaceUpdateUser(user_id, user): 
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def delete_user(user_id: Uuid):
    if InterfaceDeleteUser(user_id):  
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="User deletion failed")