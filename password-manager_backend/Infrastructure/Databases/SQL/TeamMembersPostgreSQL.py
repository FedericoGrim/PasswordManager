from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

#from Infrastructure.Exceptions.UserPostgreSQL_Exceptions import *

from Domain.Interfaces.ITeamMembers import ITeamMembersService
from Domain.Entities.TeamMembers import TeamMembers

class TeamMembersService(ITeamMembersService):
    def __init__(self, db: Session):
        self.Db = db

    def AddMemberToTeam(self, member_id: uuid.UUID, team_id: uuid.UUID, role: str) -> dict:
        try:
            new_member = TeamMembers(team_id=team_id, user_id=member_id, role=role)
            self.Db.add(new_member)
            self.Db.flush()
            self.Db.refresh(new_member)

            return new_member

        except IntegrityError:
            raise Exception("Member already exists in the team.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add member to team.")
        
    def GetTeamsByMemberId(self, member_id: uuid.UUID) -> list:
        try:
            members = self.Db.query(TeamMembers).filter(TeamMembers.user_id == member_id).all()
            return members

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve teams for the member.")
        
    def GetMembersByTeamId(self, team_id: uuid.UUID) -> list:
        try:
            members = self.Db.query(TeamMembers).filter(TeamMembers.team_id == team_id).all()
            return members

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve members for the team.")
        
    def UpdateMemberRole(self, member_id, team_id, new_role):
        try:
            member = self.Db.query(TeamMembers).filter(
                TeamMembers.user_id == member_id,
                TeamMembers.team_id == team_id
            ).first()
            
            if not member:
                raise Exception("Member not found in the team.")
            
            member.role = new_role
            self.Db.flush()
            self.Db.refresh(member)

            return member

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to update member role.")
        
    def RemoveMemberFromTeam(self, member_id, team_id):
        try:
            member = self.Db.query(TeamMembers).filter(
                TeamMembers.user_id == member_id,
                TeamMembers.team_id == team_id
            ).first()
            
            if not member:
                raise Exception("Member not found in the team.")
            
            self.Db.delete(member)
            self.Db.flush()

            return {"message": "Member removed from team successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove member from team.")