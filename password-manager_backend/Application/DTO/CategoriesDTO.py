from pydantic import BaseModel, UUID4, StringConstraints
from typing import Optional, Annotated

from Domain.Entities.Categories import Category

class CategoryDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    name: str

    def to_entity(self):
        return Category(
            team_id=self.team_id,
            name=self.name
        )

class CreateCategoryDTO(BaseModel):
    team_id: UUID4
    name: Annotated[str, StringConstraints(min_length=1)]

    def to_entity(self):
        return Category(
            team_id=self.team_id,
            name=self.name
        )
    
class UpdateCategoryDTO(BaseModel):
    name: Optional[Annotated[str, StringConstraints(min_length=1)]]

    def to_entity(self, existing_category: Category):
        return Category(
            team_id=existing_category.team_id,
            name=self.name if self.name is not None else existing_category.name
        )