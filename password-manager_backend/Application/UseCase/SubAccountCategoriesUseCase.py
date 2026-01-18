import uuid

from Application.Exceptions.SubAccountCategoriesUseCase_Exceptions import *

from Application.UseCase.Publisher import EventPublisher

class CreateSubAccountCategoryUseCase:
    def __init__(self, SubAccountCategoriesRepository, EventRepository=None):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository
        self.EventRepository = EventRepository

    def execute(self, subacc_id, category_id):
        try:
            result = self.SubAccountCategoriesRepository.CreateSubAccauntCategory(subacc_id, category_id)
        
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="SubAccountCategoryCreated",
                    Payload={
                        "subaccount_id": str(result.sub_account_id),
                        "category_id": str(result.category_id),
                    }
                )
            
            return result
            
        except Exception as e:
            raise CreateSubAccountCategoryException(str(e)) from e
        
class GetAllCategoriesBySubAccountIdUseCase:
    def __init__(self, SubAccountCategoriesRepository):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, subaccountId: uuid.UUID) -> list:
        try:
            return self.SubAccountCategoriesRepository.GetAllCategoriesBySubAccountId(subaccountId)
        except Exception as e:
            raise SubAccountCategoryRetrievalException(str(e)) from e
        
class UpdateSubAccountCategoryUseCase:
    def __init__(self, SubAccountCategoriesRepository):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, subaccountId: uuid.UUID, categoryId: uuid.UUID, new_subacc_category):
        try:
            result = self.SubAccountCategoriesRepository.UpdateSubAccauntCategory(subaccountId, categoryId, new_subacc_category.to_entity())
            return result
        except Exception as e:
            raise SubAccountCategoryUpdateException(str(e)) from e
        
class DeleteSubAccountCategoryUseCase:
    def __init__(self, SubAccountCategoriesRepository):
        self.SubAccountCategoriesRepository = SubAccountCategoriesRepository

    def execute(self, subaccountId: uuid.UUID, categoryId: uuid.UUID) -> bool:
        try:
            return self.SubAccountCategoriesRepository.DeleteSubAccauntCategory(subaccountId, categoryId)
        except Exception as e:
            raise SubAccountCategoryDeletionException(str(e)) from e