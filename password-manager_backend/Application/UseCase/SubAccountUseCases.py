import uuid

from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO
from Application.Exceptions.SubaccountUseCaseException import *

from Domain.PasswordCripting import PasswordCripting

class CreateSubAccountUseCase():
    def __init__(self, SubAccountRepository):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccount_create: CreateSubAccountDTO, salt = str):
        try:
            subaccount_create.passwordEncrypted = PasswordCripting.hashPassword(subaccount_create.passwordEncrypted, salt)
            return self.SubAccountRepository.CreateSubAccount(subaccount_create)
        except Exception as e:
            raise CreateSubaccountException(str(e)) from e
        
class GetAllSubAccountsByLocalUserIdUseCase():
    def __init__(self, SubAccountRepository):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, userId: uuid.UUID):
        try:
            return self.SubAccountRepository.GetAllSubAccountsByUserId(userId)
        except Exception as e:
            raise SubaccountRetrievalException(str(e)) from e
        
class UpdateSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccountId: uuid.UUID, new_subaccount: UpdateSubAccountDTO, salt = str):
        try:
            return self.SubAccountRepository.UpdateSubAccountById(subaccountId, new_subaccount)
        except Exception as e:
            raise SubaccountUpdateException(str(e)) from e
        
class DeleteSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccountId: uuid.UUID):
        try:
            return self.SubAccountRepository.DeleteSubAccountById(subaccountId)
        except Exception as e:
            raise SubaccountUpdateException(str(e)) from e