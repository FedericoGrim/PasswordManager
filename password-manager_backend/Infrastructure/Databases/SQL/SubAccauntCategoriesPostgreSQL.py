from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.SubAccountCategoriesPostgreSQL_Exceptions import *

from Domain.Interfaces.ISubAccountCategoriesService import ISubAccauntCategoriesService
from Domain.Entities.SubAccountCategories import SubAccountCategories

class SubAccauntCategoriesService(ISubAccauntCategoriesService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateSubAccauntCategory(self, subacc_id: str, category_id: str):
        try:
            subacc_category_entity = SubAccountCategories(
                sub_account_id = subacc_id,
                category_id = category_id
            )

            self.Db.add(subacc_category_entity)
            self.Db.flush()
            self.Db.refresh(subacc_category_entity)
            return subacc_category_entity

        except IntegrityError:
            raise SubAccauntCategoryAlreadyExistsException("SubAccauntCategory with the same subaccount and category already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccauntCategoryCreationFailedException("Failed to create subacc category.")
        
    def GetAllCategoriesBySubAccountId(self, subaccountId: uuid.UUID):
        try:
            subacc_categories: list[SubAccountCategories] = self.Db.query(SubAccountCategories).filter(SubAccountCategories.sub_account_id == subaccountId).all()
            if not subacc_categories:
                raise GetAllCategoriesBySubAccountIdNotFoundException("No categories found for the given subaccount ID.")
            return [subacc_category for subacc_category in subacc_categories]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccauntCategoryRetrievalException("Failed to retrieve subacc categories.")
        
    def UpdateSubAccauntCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID, new_subacc_category: SubAccountCategories):
        try:
            subacc_category = self.Db.query(SubAccountCategories).filter(
                SubAccountCategories.sub_account_id == subaccountId,
                SubAccountCategories.category_id == categoryId
            ).first()

            if not subacc_category:
                raise SubAccauntCategoryNotFoundException("SubAccauntCategory not found.")

            subacc_category.category_id = new_subacc_category.category_id
            self.Db.flush()
            self.Db.refresh(subacc_category)
            return subacc_category

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccauntCategoryUpdateFailedException("Failed to update subacc category.")

    def DeleteSubAccauntCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID):
        try:
            subacc_category = self.Db.query(SubAccountCategories).filter(
                SubAccountCategories.sub_account_id == subaccountId,
                SubAccountCategories.category_id == categoryId
            ).first()

            if not subacc_category:
                raise SubAccauntCategoryNotFoundException("SubAccauntCategory not found.")

            self.Db.delete(subacc_category)
            self.Db.flush()
            return True

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccauntCategoryDeletionFailedException("Failed to delete subacc category.")