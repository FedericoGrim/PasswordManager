import uuid

from application.dto.sub_account_dto import SubAccountDTO, CreateSubAccountDTO, UpdateSubAccountDTO, DeleteSubAccountDTO
from application.exceptions.sub_account_use_case_exceptions import *

from domain.interfaces.sub_account_service_interface import ISubAccountService

class CreateSubAccountUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, interactor_id: uuid.UUID, subaccount_create: CreateSubAccountDTO):
        try:
            subaccount_entity = subaccount_create.to_entity()
            result = self.SubAccountRepository.CreateSubAccount(subaccount_entity)

            return result
        except Exception as e:
            raise CreateSubAccountException(str(e)) from e
        
class GetSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, subaccountId: uuid.UUID):
        try:
            return self.SubAccountRepository.GetSubAccountById(subaccountId)
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e
        
class GetAllSubAccountsByTeamIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, teamId: uuid.UUID):
        try:
            result = self.SubAccountRepository.GetAllSubAccountsByTeamId(teamId)
            return [SubAccountDTO(
                            id=uuid.UUID(str(sub_account.id)),
                            team_id=uuid.UUID(str(sub_account.team_id)),
                            title=str(sub_account.title),
                            username=str(sub_account.username),
                            email=str(sub_account.email),
                            password=str(sub_account.password),
                            link=str(sub_account.link),
                            necessary_role=str(sub_account.necessary_role)
                            )
                        for sub_account in result]
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e
        
class UpdateSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, interactor_id: uuid.UUID, new_subaccount: UpdateSubAccountDTO) -> SubAccountDTO:
        try:
            existing_subaccount = self.SubAccountRepository.GetSubAccountById(new_subaccount.id)
            result = self.SubAccountRepository.UpdateSubAccountById(new_subaccount.to_entity(existing_subaccount))

            return SubAccountDTO(
                id=uuid.UUID(str(result.id)),
                team_id=uuid.UUID(str(result.team_id)),
                title=str(result.title),
                username=str(result.username),
                email=str(result.email),
                password=str(result.password),
                link=str(result.link),
                necessary_role=str(result.necessary_role)
            )
        
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e
        
class DeleteSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository: ISubAccountService):
        self.SubAccountRepository = SubAccountRepository

    def execute(self, interactor_id: uuid.UUID, subaccount_to_delete: DeleteSubAccountDTO):
        try:
            result = self.SubAccountRepository.DeleteSubAccountById(subaccount_to_delete.id)

            return result
        except Exception as e:
            raise SubAccountDeletionException(str(e)) from e