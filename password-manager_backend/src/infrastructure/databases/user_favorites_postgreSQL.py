from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.user_favorites_postgreSQL_exceptions import *

from domain.interfaces.user_favorite_service_interface import IUserFavoriteService
from domain.entities.user_favorite import UserFavorite

class UserFavoritesService(IUserFavoriteService):
    def __init__(self, db: Session):
        self.Db = db

    def add_favorite(self, new_favorite: UserFavorite) -> UserFavorite:
        try:
            self.Db.add(new_favorite)
            self.Db.flush()
            self.Db.refresh(new_favorite)

            return new_favorite

        except IntegrityError:
            raise Exception("This sub-account is already a favorite.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to add favorite.")

    def remove_favorite(self, user_id: uuid.UUID, sub_account_id: uuid.UUID) -> dict[str, str]:
        try:
            favorite = self.Db.query(UserFavorite).filter_by(
                user_id=user_id,
                sub_account_id=sub_account_id
            ).first()

            if not favorite:
                raise Exception("Favorite not found.")

            self.Db.delete(favorite)
            self.Db.flush()

            return {"message": "Favorite removed successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to remove favorite.")

    def get_favorites_by_user_id(self, user_id: uuid.UUID) -> list[UserFavorite]:
        try:
            favorites = self.Db.query(UserFavorite).filter_by(user_id=user_id).all()
            return favorites

        except Exception as e:
            logging.error(f"Error: {e}")
            raise Exception("Failed to retrieve favorites.")
