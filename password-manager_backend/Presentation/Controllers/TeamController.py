import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from config import Container
from Application.DTO.TeamDTO import CreateTeamDTO, UpdateTeamDTO
from Infrastructure.Databases.SQL.Database import get_db

router = APIRouter()

# -------------------- CREATE --------------------
@router.post("/")
@inject
async def ApiCreateTeam(
    team: CreateTeamDTO,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    create_team_use_case = container.SQL.team().CreateTeamProvider(
        TeamRepository__db=db,
        EventRepository=event_repo
    )

    try:
        new_team = create_team_use_case.execute(team)
        return {"message": "Team created successfully", "team_id": str(new_team.id)}
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
    team_update: UpdateTeamDTO,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_team_use_case = container.SQL.team().UpdateTeamByIdProvider(
        TeamRepository__db=db,
        EventRepository=event_repo
    )

    try:
        updated_team = update_team_use_case.execute(team_id, team_update)
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
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    delete_team_use_case = container.SQL.team().DeleteTeamByIdProvider(
        TeamRepository__db=db,
        EventRepository=event_repo
    )

    try:
        deleted = delete_team_use_case.execute(team_id)
        if deleted:
            return {"message": "Team deleted successfully"}
        raise HTTPException(status_code=400, detail="Team deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))