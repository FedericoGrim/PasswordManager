import uuid
from abc import ABC, abstractmethod

from Domain.Entities.SubAccountCategories import SubAccountCategories

@abstractmethod
class ISubAccountCategoriesService(ABC):
    @abstractmethod
    def CreateSubAccountCategory(self, subacc_id: str, category_id: str) -> dict:
        pass

    @abstractmethod
    def GetAllCategoriesBySubAccountId(self, subaccountId: uuid.UUID)  -> dict:
        pass

    @abstractmethod
    def UpdateSubAccountCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID, new_subacc_category: SubAccountCategories) -> dict:
        pass

    @abstractmethod
    def DeleteSubAccountCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID) -> dict:
        pass