from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import uuid
from dependency_injector.wiring import inject
from config import Container

from Infrastructure.Databases.SQL.Database import get_db
from Application.DTO.CategoriesDTO import CreateCategoryDTO, UpdateCategoryDTO

router = APIRouter()

@router.post("/{team_id}")
@inject
async def CreateCategory(
    categoryObj: CreateCategoryDTO,
    db: Session = Depends(get_db),
    request: Request = None,
):
    container: Container = request.app.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    create_category_use_case = container.SQL.categories().CreateCategoriesProvider(
        CategoriesRepository__db=db,
        EventRepository=event_repo
    )

    try:
        result = create_category_use_case.execute(
            categoryObj
        )
        return {"message": "Category created successfully", "category": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{team_id}")
@inject
async def GetAllCategoriesByTeamId(
    team_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    get_categories_use_case = container.SQL.categories().GetAllCategoriesByTeamIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        categories = get_categories_use_case.execute(team_id)
        return {"message": "Categories retrieved successfully", "categories": categories}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Categories not found")
    
@router.put("/{category_id}")
@inject
async def UpdateCategoryById(
    category_id: uuid.UUID, 
    updated_data: UpdateCategoryDTO, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    container: Container = request.app.container
    update_category_use_case = container.SQL.categories().UpdateCategoryByIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        result = update_category_use_case.execute(
            categoryId=category_id,
            new_category=updated_data
        )
        return {"message": "Category updated successfully", "category": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{category_id}")
@inject
async def DeleteCategory(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    request: Request = None,
):
    container: Container = request.app.container
    delete_category_use_case = container.SQL.categories().DeleteCategoryByIdProvider(
        CategoriesRepository__db=db,
    )

    try:
        if delete_category_use_case.execute(category_id):
            return {"message": "Category deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))