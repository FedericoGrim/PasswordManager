from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject

from config import Container
from Domain.Objects.UserObj import UserCreate, UserUpdate
from Infrastructure.Repositories.UserPostgreSQL import UserService, get_db

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

@router.put("/{user_id}/username")
@inject
async def ApiUpdateUserUsername(userId: uuid.UUID, 
                        newUsername: str, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    update_user_username_use_case = container.UpdateUserUsernameUseCaseProvider(UserRepository=UserService(db))
    
    try:
        user_username_updated = update_user_username_use_case.execute(userId, newUsername)
        return {"message": "User username updated successfully", "New username": user_username_updated}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{user_id}/email")
@inject
async def ApiUpdateUserEmail(userId: uuid.UUID,
                        newEmail: str, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    update_user_email_use_case = container.UpdateUserEmailUseCaseProvider(UserRepository=UserService(db))
    
    try:
        user_email_updated = update_user_email_use_case.execute(userId, newEmail)
        return {"message": "User email updated successfully", "New email": user_email_updated}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}/password")
@inject
async def ApiUpdateUserPassword(userId: uuid.UUID,
                        new_password: str, 
                        db: Session = Depends(get_db),
                        request: Request = None):
    container: Container = request.app.container
    update_user_password_use_case = container.UpdateUserPasswrordUseCaseProvider(UserRepository=UserService(db))
    
    try:
        user_password_updated = update_user_password_use_case.execute(userId, new_password)
        return {"message": "User password updated successfully", "New email": user_password_updated}
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
