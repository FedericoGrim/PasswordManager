from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from infrastructure.exceptions.sub_account_postgreSQL_exceptions import *

from domain.interfaces.sub_account_service_interface import ISubAccountService
from domain.entities.sub_account import SubAccount

class SubAccountService(ISubAccountService):
    def __init__(self, db: Session):
        self.db = db

    def create_sub_account(self, sub_account: SubAccount) -> SubAccount:
        try:
            subaccount_entity = SubAccount(
                team_id = sub_account.team_id,
                username_encrypted = sub_account.username_encrypted,
                password_encrypted = sub_account.password_encrypted,
                email_encrypted = sub_account.email_encrypted,
                site_link_encrypted = sub_account.site_link_encrypted,
                required_perm_level_id = sub_account.required_perm_level_id
            )

            self.db.add(subaccount_entity)
            self.db.flush()
            self.db.refresh(subaccount_entity)
            return subaccount_entity

        except IntegrityError:
            raise SubAccountAlreadyExistsException("SubAccount with the same name already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCreationFailedException("Failed to create sub_account.")
        
    def get_sub_account_by_id(self, sub_account_id: uuid.UUID) -> SubAccount:
        try:
            sub_account = self.db.query(SubAccount).filter(SubAccount.id == sub_account_id).first()
            if not sub_account:
                raise SubAccountNotFoundException("SubAccount not found.")
            return sub_account

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve sub_account by ID.")
    
    def get_all_sub_accounts_by_team_id(self, team_id: uuid.UUID) -> list[SubAccount]:
        try:
            subaccounts: list[SubAccount] = self.db.query(SubAccount).filter(SubAccount.team_id == team_id).all()
            if not subaccounts:
                raise GetAllSubAccountsByTeamIdNotFoundException("No subaccounts found for the given team ID.")
            return [sub_account for sub_account in subaccounts]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve subaccounts.")
        
    def update_sub_account_by_id(self, new_subaccount: SubAccount) -> SubAccount:
        try:
            sub_account = self.db.query(SubAccount).filter(SubAccount.id == new_subaccount.id).first()
            if not sub_account:
                raise SubAccountNotFoundException("SubAccount not found.")

            sub_account.username_encrypted = new_subaccount.username_encrypted
            sub_account.email_encrypted = new_subaccount.email_encrypted
            sub_account.password_encrypted = new_subaccount.password_encrypted
            sub_account.site_link_encrypted = new_subaccount.site_link_encrypted
            sub_account.required_perm_level_id = new_subaccount.required_perm_level_id
            self.db.flush()
            self.db.refresh(sub_account)
            return sub_account

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update sub_account.")
        
    def delete_sub_account_by_id(self, sub_account_id: uuid.UUID) -> dict[str, str]:
        try:
            sub_account = self.db.query(SubAccount).filter(SubAccount.id == sub_account_id).first()
            if not sub_account:
                raise SubAccountNotFoundException("SubAccount not found.")

            self.db.delete(sub_account)
            return {"message": "SubAccount deleted successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountDeletionException("Failed to delete sub_account.")