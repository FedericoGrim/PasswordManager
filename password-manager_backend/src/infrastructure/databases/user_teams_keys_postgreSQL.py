from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.user_teams_keys_postgreSQL_exceptions import *

from domain.interfaces.user_teams_keys_service_interface import IUserTeamsKeysService
from domain.entities.user_teams_keys import UserTeamsKeys
from infrastructure.databases.models.user_teams_keys_model import UserTeamsKeysModel


def _to_domain(model: UserTeamsKeysModel) -> UserTeamsKeys:
    return UserTeamsKeys(
        id=model.id,
        user_id=model.user_id,
        team_id=model.team_id,
        team_key_encrypted=model.team_key_encrypted,
    )


class UserTeamsKeysService(IUserTeamsKeysService):
    def __init__(self, db: Session):
        self.Db = db

    def add_key(self, new_key: UserTeamsKeys) -> UserTeamsKeys:
        try:
            key_model = UserTeamsKeysModel(
                user_id=new_key.user_id,
                team_id=new_key.team_id,
                team_key_encrypted=new_key.team_key_encrypted,
            )

            self.Db.add(key_model)
            self.Db.flush()
            self.Db.refresh(key_model)

            return _to_domain(key_model)

        except IntegrityError:
            raise Exception("Key already exists for this user in this team.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add key for user in team.")

    def get_key_by_id(self, key_id: uuid.UUID) -> UserTeamsKeys:
        try:
            key_model = self.Db.query(UserTeamsKeysModel).filter_by(id=key_id).first()
            if not key_model:
                raise Exception("Key not found.")
            return _to_domain(key_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve key by ID.")

    def get_keys_by_team_id(self, team_id: uuid.UUID) -> list[UserTeamsKeys]:
        try:
            key_models = self.Db.query(UserTeamsKeysModel).filter_by(team_id=team_id).all()
            return [_to_domain(key_model) for key_model in key_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve keys for the team.")

    def get_keys_by_user_id(self, user_id: uuid.UUID) -> list[UserTeamsKeys]:
        try:
            key_models = self.Db.query(UserTeamsKeysModel).filter_by(user_id=user_id).all()
            return [_to_domain(key_model) for key_model in key_models]

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve keys for the user.")

    def update_key(self, new_key_data: UserTeamsKeys) -> UserTeamsKeys:
        try:
            key_model = self.Db.query(UserTeamsKeysModel).filter_by(
                user_id=new_key_data.user_id,
                team_id=new_key_data.team_id
            ).first()

            if not key_model:
                raise Exception("Key not found for this user in this team.")

            key_model.team_key_encrypted = new_key_data.team_key_encrypted
            self.Db.flush()
            self.Db.refresh(key_model)

            return _to_domain(key_model)

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to update key.")

    def remove_key(self, user_id: uuid.UUID, team_id: uuid.UUID) -> dict[str, str]:
        try:
            key_model = self.Db.query(UserTeamsKeysModel).filter_by(
                user_id=user_id,
                team_id=team_id
            ).first()

            if not key_model:
                raise Exception("Key not found for this user in this team.")

            self.Db.delete(key_model)
            self.Db.flush()

            return {"message": "Key removed successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove key.")
