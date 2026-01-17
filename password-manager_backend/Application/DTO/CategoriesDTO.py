from pydantic import BaseModel, UUID4, StringConstraints
from typing import Optional, Annotated

from Domain.Entities.Categories import Categories

class CategoriesDTO(BaseModel):
    id: UUID4
    team_id: UUID4
    name: str

    def to_entity(self):
        return Categories(
            team_id=self.team_id,
            name=self.name
        )