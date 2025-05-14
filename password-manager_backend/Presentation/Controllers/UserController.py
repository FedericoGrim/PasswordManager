from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject

from config import Container
from Domain.Objects.UserObj import UserCreate, UserUpdate
from Infrastructure.Repositories.postgreSQL import UserService
from Infrastructure.Repositories.postgreSQL import get_db 

router = APIRouter()

@router.post("/")
@inject
async def ApiCreateUser(user: UserCreate, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    create_user_use_case = container.CreateUserUseCaseProvider(UserRepository=UserService(db))
    
    try:
        created_user = create_user_use_case.execute(user)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
@inject
async def ApiGetUser(userEmail: str, 
                     db: Session = Depends(get_db),
                     request: Request = None):
    container: Container = request.app.container
    get_user_use_case = container.GetUserUseCaseProvider(UserRepository=UserService(db))
    
    try:
        user = get_user_use_case.execute(userEmail)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
@inject
async def ApiUpdateUser(userId: uuid.UUID, 
                        userUpdated: UserUpdate, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    update_user_use_case = container.UpdateUserUseCaseProvider(UserRepository=UserService(db))
    
    try:
        user_updated = update_user_use_case.execute(userId, userUpdated)
        return {"message": "User updated successfully", "user": user_updated}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
@inject
async def ApiDeleteUser(userId: uuid.UUID, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    delete_user_use_case = container.DeleteUserUseCaseProvider(UserRepository=UserService(db))
    
    try:
        if delete_user_use_case.execute(userId):
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
