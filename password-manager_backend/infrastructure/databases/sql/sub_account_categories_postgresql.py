from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.sub_account_categories_postgresql_exceptions import *

from domain.interfaces.isub_account_categories_service import ISubAccountCategoriesService
from domain.entities.sub_account_categories import SubAccountCategories

class SubAccountCategoriesService(ISubAccountCategoriesService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateSubAccountCategory(self, new_subacc_category: SubAccountCategories) -> SubAccountCategories:
        try:
            subacc_category_entity = SubAccountCategories(
                sub_account_id = new_subacc_category.sub_account_id,
                category_id = new_subacc_category.category_id
            )

            self.Db.add(subacc_category_entity)
            self.Db.flush()
            self.Db.refresh(subacc_category_entity)
            return subacc_category_entity

        except IntegrityError:
            raise SubAccountCategoryAlreadyExistsException("SubAccountCategory with the same subaccount and category already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryCreationFailedException("Failed to create subacc category.")
        
    def GetAllCategoriesBySubAccountId(self, subaccountId: uuid.UUID) -> list[SubAccountCategories]:
        try:
            subacc_categories: list[SubAccountCategories] = self.Db.query(SubAccountCategories).filter(SubAccountCategories.sub_account_id == subaccountId).all()
            if not subacc_categories:
                raise GetAllCategoriesBySubAccountIdNotFoundException("No categories found for the given subaccount ID.")
            return [subacc_category for subacc_category in subacc_categories]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryRetrievalException("Failed to retrieve subacc categories.")

    def DeleteSubAccountCategory(self, subacc_category: SubAccountCategories) -> bool:
        try:
            subacc_category = self.Db.query(SubAccountCategories).filter(
                SubAccountCategories.sub_account_id == subacc_category.sub_account_id,
                SubAccountCategories.category_id == subacc_category.category_id
            ).first()

            if not subacc_category:
                raise SubAccountCategoryNotFoundException("SubAccountCategory not found.")

            self.Db.delete(subacc_category)
            self.Db.flush()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCategoryDeletionFailedException("Failed to delete subacc category.")