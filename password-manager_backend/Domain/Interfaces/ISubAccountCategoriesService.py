import uuid
from abc import ABC, abstractmethod

from Domain.Entities.SubAccountCategories import SubAccountCategories

@abstractmethod
class ISubAccauntCategoriesService(ABC):
    @abstractmethod
    def CreateSubAccauntCategory(self, subacc_id: str, category_id: str) -> dict:
        pass

    @abstractmethod
    def GetAllCategoriesBySubAccountId(self, subaccountId: uuid.UUID)  -> dict:
        pass

    @abstractmethod
    def UpdateSubAccauntCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID, new_subacc_category: SubAccountCategories) -> dict:
        pass

    @abstractmethod
    def DeleteSubAccauntCategory(self, subaccountId: uuid.UUID, categoryId: uuid.UUID) -> dict:
        pass