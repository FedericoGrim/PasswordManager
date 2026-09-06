from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_postgreSQL_exceptions import *

from domain.interfaces.team_service_interface import ITeamService
from domain.entities.team import Team
from domain.entities.team_member import TeamMember

class TeamService(ITeamService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateTeam(self, new_team: Team) -> Team:
        try:
            self.Db.add(new_team)
            self.Db.flush()
            self.Db.refresh(new_team)

            return new_team

        except IntegrityError:
            raise TeamAlreadyExistsException()

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamCreationFailedException()
        
    def GetTeamById(self, team_id: uuid.UUID):
        try:
            team = self.Db.query(Team).filter(Team.id == team_id).first()
            if not team:
                raise GetTeamByIdNotFoundException("No Team found for the given Team Id.")
            
            return team
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetTeamByIdRetrivalException()
        
    def GetTeamsByUserId(self, user_id: uuid.UUID):
        try:
            teams: list[Team] = self.Db.query(Team).join(TeamMember, Team.id == TeamMember.team_id).filter(TeamMember.user_id == user_id).all()
            if not teams:
                raise GetTeamsByUserIdNotFoundException("No Teams found for the given User Id.")
            return [team for team in teams]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamRetrievalException("Failed to retrieve teams.")
        
    def UpdateTeamById(self, new_team: Team) -> Team:
        try:
            team: Team = self.Db.query(Team).filter(Team.id == new_team.id).first()
            if not team:
                raise TeamNotFoundException("Team not found.")
            
            team.name = new_team.name
            self.Db.flush()
            self.Db.refresh(team)

            return team
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamUpdateException()
        
    def DeleteTeamById(self, team_id: uuid.UUID) -> dict[str, str]:
        try:
            team = self.Db.query(Team).filter(Team.id == team_id).first()
            if not team:
                raise TeamNotFoundException("Team not found.")

            self.Db.delete(team)
                
            return {"message": "Team deleted successfully."}
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamDeleteException()
        