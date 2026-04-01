from application.dto.categories_dto import CategoriesDTO
from application.use_case.publisher import EventPublisher

from application.exceptions.categories_use_case_exceptions import *

import uuid

class CreateCategoriesUseCase:
    def __init__(self, CategoriesRepository, EventRepository=None):
        self.CategoriesRepository = CategoriesRepository
        self.EventRepository = EventRepository

    def execute(self, category: CategoriesDTO):
        try:
            category_entity = category.to_entity()
            result = self.CategoriesRepository.CreateCategory(category_entity)
        
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.Publish(
                    EventType="CategoryCreated",
                    Payload={
                        "category_id": str(result.id),
                        "team_id": str(category_entity.team_id),
                        "name": category_entity.name,
                    }
                )
            
            return result
            
        except Exception as e:
            raise CreateCategoryException(str(e)) from e
        
class GetAllCategoriesByTeamIdUseCase:
    def __init__(self, CategoriesRepository):
        self.CategoriesRepository = CategoriesRepository

    def execute(self, teamId: uuid.UUID) -> list:
        try:
            return self.CategoriesRepository.GetAllCategoriesByTeamId(teamId)
        except Exception as e:
            raise CategoryRetrievalException(str(e)) from e
        
class UpdateCategoryByIdUseCase:
    def __init__(self, CategoriesRepository):
        self.CategoriesRepository = CategoriesRepository

    def execute(self, categoryId: uuid.UUID, new_category: CategoriesDTO) -> CategoriesDTO:
        try:
            result = self.CategoriesRepository.UpdateCategoryById(categoryId, new_category.to_entity())
            return result
        except Exception as e:
            raise CategoryUpdateException(str(e)) from e
        
class DeleteCategoryByIdUseCase:
    def __init__(self, CategoriesRepository):
        self.CategoriesRepository = CategoriesRepository

    def execute(self, categoryId: uuid.UUID) -> bool:
        try:
            result = self.CategoriesRepository.DeleteCategoryById(categoryId)
            return result
        except Exception as e:
            raise CategoryDeletionException(str(e)) from e