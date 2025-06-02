from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject
from config import Container

from Infrastructure.Repositories.LocalUserPostgreSQL import get_db
from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO

router = APIRouter()

@router.post("/{UserId}")
async def CreateSubAccount(
    subaccountObj: CreateSubAccountDTO,
    db: Session = Depends(get_db),
    request: Request = None,
    salt: str = ""
):
    container: Container = request.app.container
    create_subaccount_use_case = container.subaccount().CreateSubAccountProvider(SubAccountRepository__db=db)

    try:
        create_subaccount = create_subaccount_use_case.execute(subaccountObj, salt)
        return {"message": "SubAccount created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{userId}")
@inject
async def GetAllSubAccountsByUserId(userId: uuid.UUID, 
                                    db: Session = Depends(get_db), 
                                    request: Request = None):
    container: Container = request.app.container
    get_subaccounts_use_case = container.subaccount().GetAllSubAccountsByUserIdProvider(SubAccountRepository__db=db)

    try:
        subaccounts = get_subaccounts_use_case.execute(userId)
        return {"message": "SubAccounts retrieved successfully", "subaccounts": subaccounts}
    except Exception as e:
        raise HTTPException(status_code=404, detail="SubAccounts not found")

@router.put("/{userId}/{subaccountId}")
@inject
async def UpdateSubAccountById(userId: uuid.UUID, 
                               subaccountId: uuid.UUID, 
                               updated_data: UpdateSubAccountDTO, 
                               db: Session = Depends(get_db), 
                               salt: str = "",
                               request: Request = None):
    container: Container = request.app.container
    update_subaccount_use_case = container.subaccount().UpdateSubAccountByIdProvider(SubAccountRepository__db=db)

    try:
        updated_subaccount = update_subaccount_use_case.execute(userId, subaccountId, updated_data, salt)
        return {"message": "SubAccount updated successfully", "subaccount": updated_subaccount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{userId}/{subaccountId}")
@inject
async def DeleteSubAccount(userId: uuid.UUID, 
                           subaccountId: uuid.UUID, 
                           db: Session = Depends(get_db), 
                           request: Request = None):
    container: Container = request.app.container
    delete_subaccount_use_case = container.subaccount().DeleteSubAccountByIdProvider(SubAccountRepository__db=db)

    try:
        delete_subaccount = delete_subaccount_use_case.execute(userId, subaccountId)
        return {"message": "SubAccount deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))