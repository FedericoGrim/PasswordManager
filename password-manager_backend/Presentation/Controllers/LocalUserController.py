from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from uuid import UUID
from dependency_injector.wiring import inject

from config import Container
from Application.DTO.LocalUserDTO import CreateLocalUser, UpdateLocalUser
from Infrastructure.Repositories.LocalUserPostgreSQL import LocalUserService, get_db

router = APIRouter()

@router.post("/")
@inject
async def ApiCreateUser(localUser: CreateLocalUser, 
                        db: Session = Depends(get_db), 
                        request: Request = None):
    container: Container = request.app.container
    create_user_use_case = container.local_user().CreateLocalUserProvider(LocalUserRepository__db=db)

    try:
        created_user = create_user_use_case.execute(localUser)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
@inject
async def ApiGetUser(localUserId: UUID, 
                     db: Session = Depends(get_db), 
                     request: Request = None):
    container: Container = request.app.container
    get_user_use_case = container.local_user().GetAllLocalUsersByMainUserIdProvider(LocalUserRepository__db=db)
    
    try:
        user = get_user_use_case.execute(localUserId)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}")
@inject
async def ApiUpdateLocalUser(localUserId: UUID, 
                             newLocalUser: UpdateLocalUser, 
                             db: Session = Depends(get_db), 
                             request: Request = None):
    container: Container = request.app.container
    update_user_username_use_case = container.local_user().UpdateLocalUserByIdProvider(LocalUserRepository__db=db)
    
    try:
        user_username_updated = update_user_username_use_case.execute(localUserId, newLocalUser)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
@inject
async def ApiDeleteUser(keycloakId: UUID, 
                        db: Session = Depends(get_db), 
                        request: Request = None):
    container: Container = request.app.container
    delete_user_use_case = container.local_user().DeleteLocalUserByIdProvider(LocalUserRepository__db=db)
    
    try:
        if delete_user_use_case.execute(keycloakId):
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
