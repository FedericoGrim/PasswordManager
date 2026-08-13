from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.team_perm_levels_postgresql_exceptions import *

from domain.interfaces.team_perm_level_service_interface import ITeamPermLevelService
from domain.entities.team_perm_level import TeamPermLevel

class TeamPermLevelsService(ITeamPermLevelService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateTeamPermLevel(self, perm_level: TeamPermLevel) -> TeamPermLevel:
        try:
            perm_level_entity = TeamPermLevel(
                team_id = perm_level.team_id,
                name = perm_level.name,
                rank = perm_level.rank
            )

            self.Db.add(perm_level_entity)
            self.Db.flush()
            self.Db.refresh(perm_level_entity)
            return perm_level_entity

        except IntegrityError:
            raise TeamPermLevelAlreadyExistsException("Team perm level with the same name already exists for this team.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamPermLevelCreationFailedException("Failed to create team perm level.")

    def GetTeamPermLevelById(self, perm_level_id: uuid.UUID) -> TeamPermLevel:
        try:
            perm_level = self.Db.query(TeamPermLevel).filter(TeamPermLevel.id == perm_level_id).first()
            if not perm_level:
                raise TeamPermLevelNotFoundException("Team perm level not found.")
            return perm_level

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamPermLevelRetrievalException("Failed to retrieve team perm level.")

    def GetAllTeamPermLevelsByTeamId(self, teamId: uuid.UUID) -> list[TeamPermLevel]:
        try:
            perm_levels: list[TeamPermLevel] = self.Db.query(TeamPermLevel).filter(TeamPermLevel.team_id == teamId).all()
            if not perm_levels:
                raise GetAllTeamPermLevelsByTeamIdNotFoundException("No perm levels found for the given team ID.")
            return [perm_level for perm_level in perm_levels]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamPermLevelRetrievalException("Failed to retrieve team perm levels.")

    def UpdateTeamPermLevelById(self, perm_level_id: uuid.UUID, new_perm_level: TeamPermLevel) -> TeamPermLevel:
        try:
            perm_level = self.Db.query(TeamPermLevel).filter(TeamPermLevel.id == perm_level_id).first()
            if not perm_level:
                raise TeamPermLevelNotFoundException("Team perm level not found.")

            perm_level.name = new_perm_level.name
            perm_level.rank = new_perm_level.rank

            self.Db.commit()
            self.Db.refresh(perm_level)
            return perm_level

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamPermLevelUpdateException("Failed to update team perm level.")

    def DeleteTeamPermLevelById(self, perm_level_id: uuid.UUID) -> bool:
        try:
            perm_level = self.Db.query(TeamPermLevel).filter(TeamPermLevel.id == perm_level_id).first()
            if not perm_level:
                raise TeamPermLevelNotFoundException("Team perm level not found.")

            self.Db.delete(perm_level)
            self.Db.commit()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise TeamPermLevelDeletionException("Failed to delete team perm level.")
