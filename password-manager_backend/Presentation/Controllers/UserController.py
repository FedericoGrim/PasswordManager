import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject
from typing import cast

from config import Container, UserContainer, EventsContainer
from Application.DTO.UserDTO import CreateUserDTO, UpdateUserDTO
from Infrastructure.Databases.SQL.Database import get_db

router = APIRouter()

# -------------------- CREATE --------------------
@router.post("/")
@inject
async def ApiCreateUser(
    user: CreateUserDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    event_repo = cast(EventsContainer, container.NoSQL.events).EventRepositoryProvider()
    create_user_use_case = cast(UserContainer, container.SQL.user).CreateUserProvider(
        UserRepository__db=db,
        EventRepository=event_repo,
    )
    try:
        user = await create_user_use_case.execute(user)
        return {"message": "User created successfully", "user_id": str(user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- GET --------------------
@router.get("/{keycloak_user_id}")
@inject
async def ApiGetUserByKeycloakId(
    keycloak_user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    get_user_use_case = container.SQL.user().GetUserByKeycloakIdProvider(
        UserRepository__db=db
    )

    try:
        user = get_user_use_case.execute(keycloak_user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- UPDATE --------------------
@router.put("/{user_id}")
@inject
async def ApiUpdateUserById(
    user_id: uuid.UUID,
    new_user: UpdateUserDTO,
    request: Request,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_user_use_case = container.SQL.user().UpdateUserByIdProvider(
        UserRepository__db=db,
        EventRepository=event_repo
    )

    try:
        updated = await update_user_use_case.execute(user_id, new_user)
        if updated:
            return {"message": "User updated successfully"}
        raise HTTPException(status_code=400, detail="User update failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{user_id}")
@inject
async def ApiDeleteUserById(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db)
) -> dict[str, str]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    delete_user_use_case = container.SQL.user().DeleteUserByIdProvider(
        UserRepository__db=db,
        EventRepository=event_repo
    )

    try:
        deleted = await delete_user_use_case.execute(user_id)
        if deleted:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
