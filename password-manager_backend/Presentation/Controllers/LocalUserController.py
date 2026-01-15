import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from config import Container
from Application.DTO.LocalUserDTO import CreateLocalUserDTO
from Infrastructure.Databases.SQL.Database import get_db

router = APIRouter()

# -------------------- CREATE --------------------
@router.post("/")
@inject
async def ApiCreateUser(
    localUser: CreateLocalUserDTO,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    create_user_use_case = container.SQL.local_user().CreateLocalUserProvider(
        LocalUserRepository__db=db,
        EventRepository=event_repo
    )

    try:
        user = await create_user_use_case.execute(localUser)
        return {"message": "User created successfully", "user_id": str(user.Id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- GET --------------------
@router.get("/{keycloak_user_id}")
@inject
async def ApiGetUser(
    keycloak_user_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    get_user_use_case = container.SQL.local_user().GetLocalUserByKeycloakIdProvider(
        LocalUserRepository__db=db
    )

    try:
        user = get_user_use_case.execute(keycloak_user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")


# -------------------- UPDATE --------------------
@router.put("/{user_id}")
@inject
async def ApiUpdateLocalUser(
    user_id: uuid.UUID,
    salt: str,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_user_use_case = container.SQL.local_user().UpdateLocalUserByIdProvider(
        LocalUserRepository__db=db,
        EventRepository=event_repo
    )

    try:
        updated = await update_user_use_case.execute(user_id, salt.encode())
        if updated:
            return {"message": "User updated successfully"}
        raise HTTPException(status_code=400, detail="User update failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{user_id}")
@inject
async def ApiDeleteUser(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    delete_user_use_case = container.SQL.local_user().DeleteLocalUserByIdProvider(
        LocalUserRepository__db=db,
        EventRepository=event_repo
    )

    try:
        deleted = await delete_user_use_case.execute(user_id)
        if deleted:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
