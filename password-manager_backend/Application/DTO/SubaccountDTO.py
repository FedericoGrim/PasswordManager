from pydantic import BaseModel, UUID4, HttpUrl, StringConstraints
from typing import Optional, Annotated


class CreateSubAccountDTO(BaseModel):
    userId: UUID4
    title: Annotated[str, StringConstraints(min_length=1)]
    username: str
    passwordEncrypted: str
    url: str

class UpdateSubAccountDTO(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    username: Optional[str] = None
    passwordEncrypted: Optional[str] = None
    url: Optional[str] = None