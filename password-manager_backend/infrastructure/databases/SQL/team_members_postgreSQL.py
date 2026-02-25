from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_members_postgreSQL_exceptions import *

from domain.interfaces.team_members_interface import ITeamMembersService
from domain.entities.team_members import TeamMembers

class TeamMembersService(ITeamMembersService):
    def __init__(self, db: Session):
        self.Db = db

    def add_member_to_team(self, member_id: uuid.UUID, team_id: uuid.UUID, role: str) -> TeamMembers:
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
        
    def get_teams_by_member_id(self, member_id: uuid.UUID) -> list[TeamMembers]:
        try:
            members = self.Db.query(TeamMembers).filter_by(user_id=member_id).all()
            return members

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve teams for the member.")
        
    def update_member_role(self, member_id: uuid.UUID, team_id: uuid.UUID, new_role: str) -> TeamMembers:
        try:
            member = self.Db.query(TeamMembers).filter_by(
                user_id=member_id,
                team_id=team_id
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
        
    def remove_member_from_team(self, member_id: uuid.UUID, team_id: uuid.UUID) -> dict[str, str]:
        try:
            member = self.Db.query(TeamMembers).filter_by(
                user_id=member_id,
                team_id=team_id
            ).first()
            
            if not member:
                raise Exception("Member not found in the team.")
            
            self.Db.delete(member)
            self.Db.flush()

            return {"message": "Member removed from team successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove member from team.")