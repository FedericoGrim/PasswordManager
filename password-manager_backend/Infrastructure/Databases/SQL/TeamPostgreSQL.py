from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.TeamPostgreSQL_Exception import *

from Domain.Interfaces.ITeamService import ITeamService
from Domain.Entities.Team import Team

class TeamService(ITeamService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateTeam(self, new_team):
        try:
            with self.Db.begin():
                self.Db.add(new_team)
                self.Db.flush()
                self.Db.refresh(new_team)

            return new_team

        except IntegrityError:
            raise TeamAlreadyExistsException()

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamCreationFailedException()
        
    def GetTeamById(self, teamId: uuid.UUID):
        try:
            team = self.Db.query(Team).filter(Team.id == teamId).first()
            if not team:
                raise GetTeamByIdNotFoundException("No Team found for the given Team Id.")
            
            return team
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise GetTeamByIdRetrivalException()
        
    def GetTeamsByUserId(self, userId: uuid.UUID):
        try:
            teams: list[Team] = self.Db.query(Team).filter(Team.user_id == userId).all()
            if not teams:
                raise GetTeamsByUserIdNotFoundException("No Teams found for the given User Id.")
            return [team for team in teams]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamRetrievalException("Failed to retrieve teams.")
        
    def UpdateTeamById(self, teamId: uuid.UUID, new_team: Team):
        try:
            with self.Db.begin():
                team: Team = self.Db.query(Team).filter(Team.id == teamId).first()
                if not team:
                    raise TeamNotFoundException("Team not found.")
                
                team.name = new_team.name
                self.Db.flush()
                self.Db.refresh(team)

            return team
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamUpdateException()
        
    def DeleteTeamById(self, teamId: uuid.UUID):
        try:
            with self.Db.begin():
                team = self.Db.query(Team).filter(Team.id == teamId).first()
                if not team:
                    raise TeamNotFoundException("Team not found.")

                self.Db.delete(team)
                
            return {"message": "Team deleted successfully."}
        
        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamDeleteException()
        