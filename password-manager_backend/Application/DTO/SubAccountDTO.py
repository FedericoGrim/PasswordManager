from pydantic import BaseModel, UUID4, StringConstraints
from typing import Optional, Annotated


class CreateSubAccountDTO(BaseModel):
    """
    DTO for creating a subaccount.
    This class is used to transfer data for creating a new subaccount.
    """
    user_id: UUID4
    title: Annotated[str, StringConstraints(min_length=1)]
    username: str
    password_encrypted: str
    url: str

class UpdateSubAccountDTO(BaseModel):
    """
    DTO for updating a subaccount.
    This class is used to transfer data for updating an existing subaccount.
    """
    title: Optional[Annotated[str, StringConstraints(min_length=1)]] = None
    username: Optional[str] = None
    password_encrypted: Optional[str] = None
    url: Optional[str] = None
