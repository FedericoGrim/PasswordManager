import uuid
from abc import ABC, abstractmethod

from domain.entities.categories import Categories

@abstractmethod
class ICategoriesService(ABC):
    @abstractmethod
    def CreateCategory(self, category: Categories) -> Categories:
        pass

    @abstractmethod
    def GetAllCategoriesByTeamId(self, teamId: uuid.UUID) -> list[Categories]:
        pass

    @abstractmethod
    def UpdateCategoryById(self, categoryId: uuid.UUID, new_category: Categories) -> Categories:
        pass

    @abstractmethod
    def DeleteCategoryById(self, categoryId: uuid.UUID) -> bool:
        pass