from fastapi import APIRouter, HTTPException
from Domain.Objects.UserObj import UserCreate, UserUpdate
import uuid
from Application.UserInterface import InterfaceDeleteUser, InterfaceGetUser, InterfaceCreateUser, InterfaceUpdateUser

router = APIRouter()

@router.post("/")
async def CreateUser(user: UserCreate):
    created_user = InterfaceCreateUser(user)
    if created_user:
        return {"message": "User created successfully", "user": created_user}  # Restituire i dettagli dell'utente creato
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
async def UpdateUser(userId: uuid.UUID, user: UserUpdate):
    updated_user = InterfaceUpdateUser(userId, user)
    if updated_user:
        return {"message": "User updated successfully", "user": updated_user}  # Restituire i dettagli dell'utente aggiornato
    else:
        raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def DeleteUser(userId: uuid.UUID):
    if InterfaceDeleteUser(userId):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="User deletion failed")
