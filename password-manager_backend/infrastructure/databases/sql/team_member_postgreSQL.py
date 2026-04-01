from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_member_postgreSQL_exceptions import *

from domain.interfaces.team_member_service_interface import ITeamMembersService
from domain.entities.team_member import TeamMember

class TeamMembersService(ITeamMembersService):
    def __init__(self, db: Session):
        self.Db = db

    def add_member_to_team(self, new_member: TeamMember) -> TeamMember:
        try:
            self.Db.add(new_member)
            self.Db.flush()
            self.Db.refresh(new_member)

            return new_member

        except IntegrityError:
            raise Exception("Member already exists in the team.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add member to team.")
        
    def get_team_member_by_id(self, member_id: uuid.UUID) -> TeamMember:
        try:
            member = self.Db.query(TeamMember).filter_by(id=member_id).first()
            if not member:
                raise Exception("Member not found.")
            return member

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve team member by ID.")
        
    def get_teams_by_member_id(self, member_id: uuid.UUID) -> list[TeamMember]:
        try:
            members = self.Db.query(TeamMember).filter_by(user_id=member_id).all()
            return members

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve teams for the member.")
        
    def update_member_role(self, new_user_data: TeamMember) -> TeamMember:
        try:
            member = self.Db.query(TeamMember).filter_by(
                user_id=new_user_data.user_id,
                team_id=new_user_data.team_id
            ).first()
            
            if not member:
                raise Exception("Member not found in the team.")
            
            member.role = new_user_data.role
            self.Db.flush()
            self.Db.refresh(member)

            return member

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to update member role.")
        
    def remove_member_from_team(self, member_id: uuid.UUID, team_id: uuid.UUID) -> dict[str, str]:
        try:
            member = self.Db.query(TeamMember).filter_by(
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