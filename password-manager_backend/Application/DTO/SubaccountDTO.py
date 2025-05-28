from pydantic import BaseModel, UUID4, HttpUrl, StringConstraints
from typing import Optional, Annotated


class CreateSubaccountDTO(BaseModel):
    userId: UUID4
    title: Annotated[str, StringConstraints(min_length=1)]
    username: str
    passwordEncrypted: str
    url: HttpUrl

class UpdateSubaccountDTO(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    username: Optional[str] = None
    passwordEncrypted: Optional[str] = None
    url: Optional[HttpUrl] = None