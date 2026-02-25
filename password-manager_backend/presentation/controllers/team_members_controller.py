import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject

from config import Container
from infrastructure.databases.SQL.database import get_db
from application.dto.team_members_dto import TeamMembersDTO

router = APIRouter()

@router.post("/{team_id}/members")
@inject
async def api_add_member_to_team(
    interactor_id: uuid.UUID,
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    role: str,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamMembersDTO]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    add_member_use_case = container.SQL.team_members().AddMemberToTeamProvider(
        TeamMembersRepository__db=db,
        event_repository=event_repo
    )

    try:
        team_member = add_member_use_case.execute(interactor_id, member_id, team_id, role)
        return {"message": "Member added to team successfully", "team_member": team_member}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{team_id}/members")
@inject
async def api_get_team_members_by_team_id(
    team_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | list[TeamMembersDTO]]:
    container: Container = request.app.state.container
    get_members_use_case = container.SQL.team_members().GetTeamMembersByTeamIdProvider(
        TeamMembersRepository__db=db
    )

    try:
        team_members = get_members_use_case.execute(team_id)
        return {"message": "Team members retrieved successfully", "team_members": team_members}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{team_id}/members/{member_id}/role")
@inject
async def api_update_team_member_role(
    user_interactor: uuid.UUID,
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    new_role: str,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str | TeamMembersDTO]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_role_use_case = container.SQL.team_members().UpdateTeamMemberRoleProvider(
        TeamMembersRepository__db=db,
        event_repository=event_repo
    )

    try:
        updated_member = update_role_use_case.execute(user_interactor, member_id, team_id, new_role)
        return {"message": "Team member role updated successfully", "updated_member": updated_member}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{team_id}/members/{member_id}")
@inject
async def api_remove_member_from_team(
    interactor_id: uuid.UUID,
    team_id: uuid.UUID,
    member_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    remove_member_use_case = container.SQL.team_members().RemoveMemberFromTeamProvider(
        TeamMembersRepository__db=db,
        event_repository=event_repo
    )

    try:
        remove_member_use_case.execute(interactor_id, member_id, team_id)
        return {"message": "Member removed from team successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))