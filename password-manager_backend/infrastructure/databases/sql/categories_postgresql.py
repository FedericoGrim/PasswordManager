from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.categories_postgresql_exceptions import *

from domain.interfaces.icategories import ICategoriesService
from domain.entities.categories import Categories

class CategoriesService(ICategoriesService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateCategory(self, category):
        try:
            category_entity = Categories(
                team_id = category.team_id,
                name = category.name
            )

            self.Db.add(category_entity)
            self.Db.flush()
            self.Db.refresh(category_entity)
            return category_entity

        except IntegrityError:
            raise CategoryAlreadyExistsException("Category with the same name already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryCreationFailedException("Failed to create category.")
        
    def GetAllCategoriesByTeamId(self, teamId: uuid.UUID):
        try:
            categories: list[Categories] = self.Db.query(Categories).filter(Categories.team_id == teamId).all()
            if not categories:
                raise GetAllCategoriesByTeamIdNotFoundException("No categories found for the given team ID.")
            return [category for category in categories]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryRetrievalException("Failed to retrieve categories.")
        
    def UpdateCategoryById(self, categoryId: uuid.UUID, new_category: Categories):
        try:
            category = self.Db.query(Categories).filter(Categories.id == categoryId).first()
            if not category:
                raise CategoryNotFoundException("Category not found.")

            category.name = new_category.name

            self.Db.commit()
            self.Db.refresh(category)
            return category

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryUpdateException("Failed to update category.")

    def DeleteCategoryById(self, categoryId: uuid.UUID):
        try:
            category = self.Db.query(Categories).filter(Categories.id == categoryId).first()
            if not category:
                raise CategoryNotFoundException("Category not found.")

            self.Db.delete(category)
            self.Db.commit()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise CategoryDeletionException("Failed to delete category.")