from application.dto.categories_dto import *
from application.use_case.publisher import EventPublisher

from application.exceptions.categories_use_case_exceptions import *

from domain.interfaces.icategories import ICategoriesService
from domain.interfaces.events_mongoDB_interface import IEventsMongoDB

import uuid

class CreateCategoriesUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService, EventRepository: IEventsMongoDB):
        self.CategoriesRepository = CategoriesRepository
        self.EventRepository = EventRepository

    def execute(self, category: CreateCategoryDTO, user_interactor_id: uuid.UUID) -> CategoriesDTO:
        try:
            category_entity = category.to_entity()
            result = self.CategoriesRepository.CreateCategory(category_entity)
        
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.publish(
                    event_type="CategoryCreated",
                    payload={
                        "category_id": str(result.id),
                        "team_id": str(category_entity.team_id),
                        "name": category_entity.name,
                    },
                    user_id=user_interactor_id,
                )
            
            return result
            
        except Exception as e:
            raise CreateCategoryException(str(e)) from e
        
class GetAllCategoriesByTeamIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService):
        self.CategoriesRepository = CategoriesRepository

    def execute(self, teamId: uuid.UUID) -> list[CategoriesDTO]:
        try:
            categories = self.CategoriesRepository.GetAllCategoriesByTeamId(teamId)
            return [
                CategoriesDTO(
                    id=uuid.UUID(str(category.id)),
                    team_id=uuid.UUID(str(category.team_id)),
                    name=str(category.name)
                )
                for category in categories
            ]
        except Exception as e:
            raise CategoryRetrievalException(str(e)) from e
        
class UpdateCategoryByIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService, EventRepository: IEventsMongoDB):
        self.CategoriesRepository = CategoriesRepository
        self.EventRepository = EventRepository

    def execute(self, categoryId: uuid.UUID, new_category: UpdateCategoryDTO, user_interactor_id: uuid.UUID):
        try:
            result = self.CategoriesRepository.UpdateCategoryById(categoryId, new_category.to_entity())

            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.publish(
                    event_type="CategoryUpdated",
                    payload={
                        "category_id": str(result.id),
                        "team_id": str(result.team_id),
                        "name": result.name,
                    },
                    user_id=user_interactor_id,
                )
                
                return CategoriesDTO(
                    id=uuid.UUID(str(result.id)),
                    team_id=uuid.UUID(str(result.team_id)),
                    name=str(result.name)
                )
            
        except Exception as e:
            raise CategoryUpdateException(str(e)) from e
        
class DeleteCategoryByIdUseCase:
    def __init__(self, CategoriesRepository: ICategoriesService, EventRepository: IEventsMongoDB):
        self.CategoriesRepository = CategoriesRepository
        self.EventRepository = EventRepository

    def execute(self, categoryId: uuid.UUID, user_interactor_id: uuid.UUID) -> bool:
        try:
            result = self.CategoriesRepository.DeleteCategoryById(categoryId)
            
            if self.EventRepository:
                publisher = EventPublisher(self.EventRepository)
                publisher.publish(
                    event_type="CategoryDeleted",
                    payload={
                        "category_id": str(categoryId),
                    },
                    user_id=user_interactor_id,
                )
            
            return result
        except Exception as e:
            raise CategoryDeletionException(str(e)) from e