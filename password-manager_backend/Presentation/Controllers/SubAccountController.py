from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject
from config import Container

from Infrastructure.Databases.SQL.Database import get_db
from Application.DTO.SubAccountDTO import CreateSubAccountDTO, UpdateSubAccountDTO

router = APIRouter()

@router.post("/{user_id}")
async def CreateSubAccount(
    subaccountObj: CreateSubAccountDTO,
    db: Session = Depends(get_db),
    request: Request = None,
):
    '''
    Create a new subaccount for a user.
    
    Args:
        subaccountObj (CreateSubAccountDTO): The subaccount data to be created.
        db (Session): The database session.
        request (Request): The FastAPI request object.
        salt (str): Optional salt for password hashing.
    
    Returns:
        dict: A message indicating success or failure.
        
    Raises: 
        HTTPException: If the subaccount creation fails.
    '''
    container: Container = request.app.container
    create_subaccount_use_case = container.SQL.subaccount().CreateSubAccountProvider(SubAccountRepository__db=db)

    try:
        if create_subaccount_use_case.execute(subaccountObj):
            return {"message": "SubAccount created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}")
@inject
async def GetAllSubAccountsByUserId(
    user_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    '''
    Retrieve all subaccounts for a given user ID.

    Args:
        userId (uuid.UUID): The ID of the user whose subaccounts are to be retrieved
        db (Session): The database session.
        request (Request): The FastAPI request object.

    Returns:
        dict: A message indicating success and the list of subaccounts.

    Raises:
        HTTPException: If the subaccounts are not found or an error occurs.
    '''
    container: Container = request.app.container
    get_subaccounts_use_case = container.SQL.subaccount().GetAllSubAccountsByUserIdProvider(SubAccountRepository__db=db)

    try:
        subaccounts = get_subaccounts_use_case.execute(user_id)
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
    '''
    Update a subaccount by its ID.
    
    Args:
        userId (uuid.UUID): The ID of the user who owns the subaccount.
        subaccountId (uuid.UUID): The ID of the subaccount to be updated.
        updated_data (UpdateSubAccountDTO): The new data for the subaccount.
        db (Session): The database session.
        salt (str): Optional salt for password hashing.
        request (Request): The FastAPI request object.
        
    Returns:
        dict: A message indicating success and the updated subaccount data.

    Raises:
        HTTPException: If the subaccount update fails.
    '''

    container: Container = request.app.container
    update_subaccount_use_case = container.SQL.subaccount().UpdateSubAccountByIdProvider(SubAccountRepository__db=db)

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
    '''
    Delete a subaccount by its ID.
    
    Args:
        userId (uuid.UUID): The ID of the user who owns the subaccount.
        subaccountId (uuid.UUID): The ID of the subaccount to be deleted.
        db (Session): The database session.
        request (Request): The FastAPI request object.
    
    Returns:
        dict: A message indicating success or failure.
        
    Raises:
        HTTPException: If the subaccount deletion fails.
    '''
    container: Container = request.app.container
    delete_subaccount_use_case = container.SQL.subaccount().DeleteSubAccountByIdProvider(SubAccountRepository__db=db)

    try:
        if delete_subaccount_use_case.execute(subaccount_id):
            return {"message": "SubAccount deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
