import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from config import Container
from Application.DTO.TeamDTO import CreateTeamDTO
from Infrastructure.Databases.SQL.Database import get_db

router = APIRouter()

# -------------------- CREATE --------------------
@router.post("/")
@inject
async def ApiCreateTeam(
    team: CreateTeamDTO,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = None,
    request: Request = None
):
    container: Container = request.app.container
    create_team_use_case = container.SQL.team().CreateTeamProvider(
        TeamRepository__db=db
    )

    try:
        new_team = await create_team_use_case.execute(team, user_id)
        return {"message": "Team created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# -------------------- GET --------------------
@router.get("/{team_id}")
@inject
async def ApiGetTeamById(
    team_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    get_team_use_case = container.SQL.team().GetTeamByIdProvider(
        TeamRepository__db=db
    )

    try:
        team = get_team_use_case.execute(team_id)
        return {"message": "Team retrieved successfully", "team": team}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Team not found")
    
@router.get("/{user_id}")
@inject
async def ApiGetTeamsByUserId(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    get_teams_use_case = container.SQL.team().GetTeamsByUserIdProvider(
        TeamRepository__db=db
    )

    try:
        teams = get_teams_use_case.execute(user_id)
        return {"message": "Teams retrieved successfully", "teams": teams}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Teams not found")
    
# -------------------- UPDATE --------------------
@router.put("/{team_id}")
@inject
async def ApiUpdateTeam(
    team_id: uuid.UUID,
    name: str,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    update_team_use_case = container.SQL.team().UpdateTeamByIdProvider(
        TeamRepository__db=db
    )

    try:
        updated_team = await update_team_use_case.execute(team_id, name)
        return {"message": "Team updated successfully", "team": updated_team}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# -------------------- DELETE --------------------
@router.delete("/{team_id}")
@inject
async def ApiDeleteTeam(
    team_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    delete_team_use_case = container.SQL.team().DeleteTeamByIdProvider(
        TeamRepository__db=db
    )

    try:
        deleted = await delete_team_use_case.execute(team_id)
        if deleted:
            return {"message": "Team deleted successfully"}
        raise HTTPException(status_code=400, detail="Team deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))