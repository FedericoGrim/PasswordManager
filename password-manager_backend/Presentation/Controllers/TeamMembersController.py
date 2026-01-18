import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from config import Container
from Infrastructure.Databases.SQL.Database import get_db

router = APIRouter()

@router.post("/{team_id}/members")
@inject
async def ApiAddMemberToTeam(
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    role: str,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    add_member_use_case = container.SQL.team_members().AddMemberToTeamProvider(
        TeamMembersRepository__db=db,
        EventRepository=event_repo
    )

    try:
        team_member = add_member_use_case.execute(member_id, team_id, role)
        return {"message": "Member added to team successfully", "team_member": team_member}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{team_id}/members")
@inject
async def ApiGetTeamMembersByTeamId(
    team_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    get_members_use_case = container.SQL.team_members().GetTeamMembersByTeamIdProvider(
        TeamMembersRepository__db=db
    )

    try:
        team_members = get_members_use_case.execute(team_id)
        return {"message": "Team members retrieved successfully", "team_members": team_members}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/members/{member_id}/teams")
@inject
async def ApiGetTeamsByMemberId(
    member_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    get_teams_use_case = container.SQL.team_members().GetTeamsByMemberIdProvider(
        TeamMembersRepository__db=db
    )

    try:
        teams = get_teams_use_case.execute(member_id)
        return {"message": "Teams retrieved successfully", "teams": teams}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{team_id}/members/{member_id}/role")
@inject
async def ApiUpdateTeamMemberRole(
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    new_role: str,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_role_use_case = container.SQL.team_members().UpdateTeamMemberRoleProvider(
        TeamMembersRepository__db=db,
        EventRepository=event_repo
    )

    try:
        updated_member = update_role_use_case.execute(member_id, team_id, new_role)
        return {"message": "Team member role updated successfully", "updated_member": updated_member}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{team_id}/members/{member_id}")
@inject
async def ApiRemoveMemberFromTeam(
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    remove_member_use_case = container.SQL.team_members().RemoveMemberFromTeamProvider(
        TeamMembersRepository__db=db,
        EventRepository=event_repo
    )

    try:
        remove_member_use_case.execute(member_id, team_id)
        return {"message": "Member removed from team successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))