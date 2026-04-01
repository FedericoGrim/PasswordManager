import uuid
from abc import ABC, abstractmethod

@abstractmethod
class ICategoriesService(ABC):
    @abstractmethod
    def CreateCategory(self, category):
        pass

    @abstractmethod
    def GetAllCategoriesByTeamId(self, teamId: uuid.UUID):
        pass

    @abstractmethod
    def UpdateCategoryById(self, categoryId: uuid.UUID, new_category):
        pass

    @abstractmethod
    def DeleteCategoryById(self, categoryId: uuid.UUID):
        pass