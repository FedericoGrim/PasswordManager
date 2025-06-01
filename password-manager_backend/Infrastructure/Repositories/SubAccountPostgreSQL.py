from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import os
import uuid
from dotenv import load_dotenv
import logging

from Infrastructure.Exceptions.SubAccountPostgreSQL_Exceptions import *

from Domain.ISubAccountService import ISubAccountService
from Domain.Entities.SubAccount import SubAccount

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    except Exception as e:
        logging.error(f"Error: {e}")
        raise PostgreSqlConnectionException()
    
    finally:
        db.close()


class SubAccountService(ISubAccountService):
    def __init__(self, db: Session):
        self.Db = db

    def CreateSubAccount(self, subaccount):
        try:
            self.Db.add(subaccount)
            self.Db.commit()
            self.Db.refresh(subaccount)
            return subaccount
            
        except IntegrityError:
            self.Db.rollback()
            raise SubAccountAlreadyExistsException("SubAccount with the same name already exists.")
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountCreationFailedException("Failed to create subaccount.")
        
    def GetAllSubAccountsByUserId(self, userId: uuid.UUID):
        try:
            subaccounts = self.Db.query(SubAccount).filter(SubAccount.user_id == userId).all()
            if not subaccounts:
                raise GetAllSubAccountsByUserIdNotFoundException("No subaccounts found for the given user ID.")
            return [subaccount for subaccount in subaccounts]
            
        except Exception as e:
            logging.error(f"Error: {e}")
            raise SubAccountRetrievalException("Failed to retrieve subaccounts.")
        
    def UpdateSubAccountById(self, subaccountId: uuid.UUID, new_subaccount):
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")
            
            for key, value in new_subaccount.to_dict().items():
                setattr(subaccount, key, value)
                
            self.Db.commit()
            return subaccount
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountUpdateException("Failed to update subaccount.")
        
    def DeleteSubAccountById(self, subaccountId: uuid.UUID):
        try:
            subaccount = self.Db.query(SubAccount).filter(SubAccount.id == subaccountId).first()
            if not subaccount:
                raise SubAccountNotFoundException("SubAccount not found.")
            
            self.Db.delete(subaccount)
            self.Db.commit()
            return {"message": "SubAccount deleted successfully."}
            
        except Exception as e:
            self.Db.rollback()
            logging.error(f"Error: {e}")
            raise SubAccountDeletionException("Failed to delete subaccount.")