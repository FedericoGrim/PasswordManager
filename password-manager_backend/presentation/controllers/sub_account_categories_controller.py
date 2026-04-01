from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject
from config import Container

from infrastructure.databases.sql.database import get_db

router = APIRouter()

@router.post("/")
@inject
async def CreateSubAccauntCategory(
    subacc_id: str,
    category_id: str,
    db: Session = Depends(get_db),
    request: Request = None,
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    create_subacc_category_use_case = container.SQL.sub_account_categories().CreateSubAccountCategoryProvider(
        SubAccountCategoriesRepository__db=db,
        EventRepository=event_repo
    )

    try:
        result = create_subacc_category_use_case.execute(
            subacc_id,
            category_id
        )
        return {"message": "SubAccountCategory created successfully", "subacc_category": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{subaccount_id}")
@inject
async def GetAllCategoriesBySubAccountId(
    subaccount_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    get_subacc_categories_use_case = container.SQL.sub_account_categories().GetAllCategoriesBySubAccountIdProvider(
        SubAccountCategoriesRepository__db=db,
    )

    try:
        subacc_categories = get_subacc_categories_use_case.execute(subaccount_id)
        return {"message": "SubAccountCategories retrieved successfully", "subacc_categories": subacc_categories}
    except Exception as e:
        raise HTTPException(status_code=404, detail="SubAccountCategories not found")
    
@router.put("/{subaccount_id}/{category_id}")
@inject
async def UpdateSubAccauntCategory(
    subaccount_id: uuid.UUID, 
    category_id: uuid.UUID,
    updated_data: dict,
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    update_subacc_category_use_case = container.SQL.sub_account_categories().UpdateSubAccountCategoryProvider(
        SubAccountCategoriesRepository__db=db,
    )

    try:
        result = update_subacc_category_use_case.execute(
            subaccount_id,
            category_id,
            updated_data
        )
        return {"message": "SubAccountCategory updated successfully", "subacc_category": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{subaccount_id}/{category_id}")
@inject
async def DeleteSubAccauntCategory(
    subaccount_id: uuid.UUID, 
    category_id: uuid.UUID,
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    delete_subacc_category_use_case = container.SQL.sub_account_categories().DeleteSubAccountCategoryProvider(
        SubAccountCategoriesRepository__db=db,
    )

    try:
        result = delete_subacc_category_use_case.execute(
            subaccount_id,
            category_id
        )
        return {"message": "SubAccountCategory deleted successfully", "success": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))