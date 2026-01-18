from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
import logging

from Infrastructure.Exceptions.SubAccountPostgreSQL_Exceptions import *

from Domain.Interfaces.ISubAccountService import ISubAccountService
from Domain.Entities.SubAccount import SubAccount

class SubAccountService(ISubAccountService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateSubAccount(self, subaccount):
        try:
            subaccount_entity = SubAccount(
                team_id = subaccount.team_id,
                title = subaccount.title,
                username = subaccount.username,
                password = subaccount.password,
                email = subaccount.email,
                link = subaccount.link,
                necessary_role = subaccount.necessary_role
            )

            self.Db.add(subaccount_entity)
            self.Db.flush()
            self.Db.refresh(subaccount_entity)
            return subaccount_entity

        except IntegrityError:
            raise SubAccountAlreadyExistsException("SubAccount with the same name already exists.")

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountCreationFailedException("Failed to create subaccount.")
        
    def GetAllSubAccountsByTeamId(self, teamId: uuid.UUID):
        try:
            subaccounts: list[SubAccount] = self.Db.query(SubAccount).filter(SubAccount.team_id == teamId).all()
            if not subaccounts:
                raise GetAllSubAccountsByTeamIdNotFoundException("No subaccounts found for the given user ID.")
            return [subaccount for subaccount in subaccounts]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve subaccounts.")
        
    def UpdateSubAccountById(self, subaccountId: uuid.UUID, new_subaccount: SubAccount):
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")

            subaccount.title = new_subaccount.title
            subaccount.username = new_subaccount.username
            subaccount.email = new_subaccount.email
            subaccount.password = new_subaccount.password
            subaccount.link = new_subaccount.link
            subaccount.necessary_role = new_subaccount.necessary_role
            self.Db.flush()
            self.Db.refresh(subaccount)
            return subaccount

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update subaccount.")
        
    def DeleteSubAccountById(self, subaccountId: uuid.UUID):
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")

            self.Db.delete(subaccount)
            return {"message": "SubAccount deleted successfully."}

        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountDeletionException("Failed to delete subaccount.")