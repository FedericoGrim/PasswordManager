from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from Infrastructure.Repositories.LocalUserPostgreSQL import get_db
from Application.DTO.SubaccountDTO import CreateSubaccountDTO, UpdateSubaccountDTO
from Domain.Entities.Subaccount import Subaccount  # suppongo questo sia il modello ORM

router = APIRouter(prefix="/subaccounts", tags=["Subaccounts"])

@router.post("/{userId}", status_code=status.HTTP_201_CREATED)
async def CreateSubaccount(userId: uuid.UUID, subaccount: CreateSubaccountDTO, db: Session = Depends(get_db)):
    new_subaccount = Subaccount(
        user_id=userId,
        title=subaccount.Title,
        username=subaccount.Username,
        password_encrypted=subaccount.PasswordEncrypted,
        url=subaccount.Url
    )
    db.add(new_subaccount)
    db.commit()
    db.refresh(new_subaccount)
    return {"message": "Subaccount created", "subaccountId": new_subaccount.id}

@router.get("/{userId}")
async def GetAllSubaccountsByUserId(userId: uuid.UUID, db: Session = Depends(get_db)):
    subaccounts = db.query(Subaccount).filter(Subaccount.user_id == userId).all()
    if not subaccounts:
        raise HTTPException(status_code=404, detail="No subaccounts found for this user")
    return subaccounts

@router.put("/{userId}/{subaccountId}")
async def UpdateSubaccountById(userId: uuid.UUID, subaccountId: uuid.UUID, updated_data: UpdateSubaccountDTO, db: Session = Depends(get_db)):
    subaccount = db.query(Subaccount).filter(Subaccount.id == subaccountId, Subaccount.user_id == userId).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="Subaccount not found")

    for field, value in updated_data.dict(exclude_unset=True).items():
        # Assicurati che i nomi campi DTO corrispondano a quelli dell'entity
        setattr(subaccount, field.lower(), value)
    db.commit()
    return {"message": "Subaccount updated"}

@router.delete("/{userId}/{subaccountId}", status_code=status.HTTP_204_NO_CONTENT)
async def DeleteSubaccount(userId: uuid.UUID, subaccountId: uuid.UUID, db: Session = Depends(get_db)):
    subaccount = db.query(Subaccount).filter(Subaccount.id == subaccountId, Subaccount.user_id == userId).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="Subaccount not found")

    db.delete(subaccount)
    db.commit()
    return
