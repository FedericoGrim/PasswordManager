import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from config import Container

from infrastructure.databases.database import get_db

from application.dto.user_teams_keys_dto import UserTeamsKeyDTO, CreateUserTeamsKeyDTO, UpdateUserTeamsKeyDTO, RemoveUserTeamsKeyDTO

router = APIRouter()

@router.post("/{team_id}/keys")

async def api_add_user_teams_key(
    interactor_id: uuid.UUID,
    CreateUserTeamsKeyDTO: CreateUserTeamsKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | UserTeamsKeyDTO]:
    container: Container = request.app.state.container
    add_key_use_case = container.user_teams_keys().AddUserTeamsKeyProvider(
        UserTeamsKeysRepository__db=db,
    )

    try:
        user_teams_key = add_key_use_case.execute(interactor_id, CreateUserTeamsKeyDTO)
        return {"message": "Key added successfully", "user_teams_key": user_teams_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/keys/{key_id}")

async def api_get_user_teams_key_by_id(
    key_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | UserTeamsKeyDTO]:
    container: Container = request.app.state.container
    get_key_use_case = container.user_teams_keys().GetUserTeamsKeyByIdProvider(
        UserTeamsKeysRepository__db=db
    )

    try:
        user_teams_key = get_key_use_case.execute(key_id)
        return {"message": "Key retrieved successfully", "user_teams_key": user_teams_key}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{team_id}/keys")

async def api_get_user_teams_keys_by_team_id(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | list[UserTeamsKeyDTO]]:
    container: Container = request.app.state.container
    get_keys_use_case = container.user_teams_keys().GetUserTeamsKeysByTeamIdProvider(
        UserTeamsKeysRepository__db=db
    )

    try:
        user_teams_keys = get_keys_use_case.execute(team_id)
        return {"message": "Keys retrieved successfully", "user_teams_keys": user_teams_keys}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/user/{user_id}/keys")

async def api_get_user_teams_keys_by_user_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | list[UserTeamsKeyDTO]]:
    container: Container = request.app.state.container
    get_keys_use_case = container.user_teams_keys().GetUserTeamsKeysByUserIdProvider(
        UserTeamsKeysRepository__db=db
    )

    try:
        user_teams_keys = get_keys_use_case.execute(user_id)
        return {"message": "Keys retrieved successfully", "user_teams_keys": user_teams_keys}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{team_id}/keys/{user_id}")

async def api_update_user_teams_key(
    interactor_id: uuid.UUID,
    new_key_data: UpdateUserTeamsKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | UserTeamsKeyDTO]:
    container: Container = request.app.state.container
    update_key_use_case = container.user_teams_keys().UpdateUserTeamsKeyProvider(
        UserTeamsKeysRepository__db=db,
    )

    try:
        updated_key = update_key_use_case.execute(interactor_id, new_key_data)
        return {"message": "Key updated successfully", "updated_key": updated_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{team_id}/keys/{user_id}")

async def api_remove_user_teams_key(
    interactor_id: uuid.UUID,
    key_to_delete: RemoveUserTeamsKeyDTO,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    remove_key_use_case = container.user_teams_keys().RemoveUserTeamsKeyProvider(
        UserTeamsKeysRepository__db=db,
    )

    try:
        remove_key_use_case.execute(interactor_id, key_to_delete)
        return {"message": "Key removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
