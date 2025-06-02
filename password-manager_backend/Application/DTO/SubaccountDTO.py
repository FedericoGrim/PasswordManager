from pydantic import BaseModel, UUID4, StringConstraints
from typing import Optional, Annotated


class CreateSubAccountDTO(BaseModel):
    user_id: UUID4
    title: Annotated[str, StringConstraints(min_length=1)]
    username: str
    password_encrypted: str
    url: str

class UpdateSubAccountDTO(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    username: Optional[str] = None
    password_encrypted: Optional[str] = None
    url: Optional[str] = None