from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject
from config import Container

from Infrastructure.Databases.SQL.Database import get_db
from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO

router = APIRouter()

@router.post("/{team_id}")
async def CreateSubAccount(
    subaccountObj: CreateSubAccountDTO,
    db: Session = Depends(get_db),
    request: Request = None,
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    create_subaccount_use_case = container.SQL.subaccount().CreateSubAccountProvider(
        SubAccountRepository__db=db,
        EventRepository=event_repo
    )

    try:
        if create_subaccount_use_case.execute(subaccountObj):
            return {"message": "SubAccount created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{team_id}")
@inject
async def GetAllSubAccountsByTeamId(
    team_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    get_subaccounts_use_case = container.SQL.subaccount().GetAllSubAccountsByTeamIdProvider(
        SubAccountRepository__db=db,
    )

    try:
        subaccounts = get_subaccounts_use_case.execute(team_id)
        return {"message": "SubAccounts retrieved successfully", "subaccounts": subaccounts}
    except Exception as e:
        raise HTTPException(status_code=404, detail="SubAccounts not found")

@router.put("/{subaccount_id}")
@inject
async def UpdateSubAccountById(
    subaccount_id: uuid.UUID, 
    updated_data: UpdateSubAccountDTO, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_subaccount_use_case = container.SQL.subaccount().UpdateSubAccountByIdProvider(
        SubAccountRepository__db=db,
        EventRepository=event_repo
    )

    try:
        if update_subaccount_use_case.execute( subaccount_id, updated_data):
            return {"message": "SubAccount updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{subaccount_id}")
@inject
async def DeleteSubAccount(
    subaccount_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    delete_subaccount_use_case = container.SQL.subaccount().DeleteSubAccountByIdProvider(
        SubAccountRepository__db=db,
        EventRepository=event_repo
    )

    try:
        if delete_subaccount_use_case.execute(subaccount_id):
            return {"message": "SubAccount deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
