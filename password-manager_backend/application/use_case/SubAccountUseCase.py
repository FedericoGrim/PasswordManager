import uuid

from Application.DTO.SubAccountDTO import SubAccountDTO, CreateSubAccountDTO, UpdateSubAccountDTO
from Application.Exceptions.SubAccountUseCaseException import *

from Application.UseCase.Publisher import EventPublisher

class CreateSubAccountUseCase():
    def __init__(self, SubAccountRepository, EventRepository=None):
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccount_create: CreateSubAccountDTO):
        try:
            subaccount_entity = subaccount_create.to_entity()
            result = self.SubAccountRepository.CreateSubAccount(subaccount_entity)
            
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="SubAccountCreated",
                    Payload={
                        "subaccount_id": str(result.id),
                        "title": subaccount_create.title,
                        "user_name": subaccount_create.username,
                        "email": subaccount_create.email,
                        "password": subaccount_create.password,
                        "link": subaccount_create.link,
                        "necessary_role": subaccount_create.necessary_role
                    }
                )
            
            return result
        except Exception as e:
            raise CreateSubAccountException(str(e)) from e
        
class GetAllSubAccountsByTeamIdUseCase():
    def __init__(self, SubAccountRepository):
        self.SubAccountRepository = SubAccountRepository
        
    def execute(self, teamId: uuid.UUID):
        try:
            return self.SubAccountRepository.GetAllSubAccountsByTeamId(teamId)
        except Exception as e:
            raise SubAccountRetrievalException(str(e)) from e
        
class UpdateSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository, EventRepository=None):
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccountId: uuid.UUID, new_subaccount: SubAccountDTO):
        try:
            result = self.SubAccountRepository.UpdateSubAccountById(subaccountId, new_subaccount)
            
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="SubAccountUpdated",
                    Payload={
                        "subaccount_id": str(subaccountId),
                        "title": new_subaccount.title,
                        "username": new_subaccount.username,
                        "email": new_subaccount.email,
                        "password": new_subaccount.password,
                        "link": new_subaccount.link,
                        "necessary_role": new_subaccount.necessary_role
                    }
                )
            
            return result
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e
        
class DeleteSubAccountByIdUseCase():
    def __init__(self, SubAccountRepository, EventRepository=None):
        self.SubAccountRepository = SubAccountRepository
        self.EventRepository = EventRepository
        
    def execute(self, subaccountId: uuid.UUID):
        try:
            result = self.SubAccountRepository.DeleteSubAccountById(subaccountId)
            
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="SubAccountDeleted",
                    Payload={
                        "subaccount_id": str(subaccountId),
                    }
                )
            
            return result
        except Exception as e:
            raise SubAccountUpdateException(str(e)) from e