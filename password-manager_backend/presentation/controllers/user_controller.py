import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session


from config import Container
from application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserDTO
from infrastructure.databases.sql.database import get_db
from infrastructure.keycloak.jwt_token_autentication import jwt_authentication

router = APIRouter()


# -------------------- CREATE --------------------
@router.post("/")
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user_payload: dict[str, str] = Depends(jwt_authentication) 
) -> dict[str, str| UserDTO]:
    container: Container = request.app.state.container
    
    # Estraiamo il keycloak_id (sub) dal payload del token
    keycloak_id = current_user_payload.get("sub")
    
    # Creiamo il DTO internamente con i dati certi del token
    try:
        if not keycloak_id:
            raise ValueError("keycloak_id not found in token")
        user_dto = CreateUserDTO(id_keycloak=uuid.UUID(keycloak_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data: {str(e)}")
    
    create_user_use_case = container.sql.user().CreateUserProvider(
        UserRepository__db=db,
        event_repository=container.NoSQL.events().EventRepositoryProvider(),
    )
    
    try:
        user = await create_user_use_case.execute(user_dto)
        return {"message": "User created successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# -------------------- GET --------------------
@router.get("/me")
async def get_my_user_data(
    request: Request,
    db: Session = Depends(get_db),
    current_user_payload: dict[str, str] = Depends(jwt_authentication) 
) -> dict[str, str| UserDTO]:
    keycloak_id = current_user_payload.get("sub")
    if not keycloak_id:
        raise HTTPException(status_code=400, detail="keycloak_id not found in token")

    container: Container = request.app.state.container
    get_user_use_case = container.sql.user().GetUserByKeycloakIdProvider(
        UserRepository__db=db
    )

    try:
        user = get_user_use_case.execute(uuid.UUID(keycloak_id))
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{keycloak_user_id}")
async def get_user_by_keycloak_id(
    keycloak_user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str| UserDTO]:
    container: Container = request.app.state.container
    get_user_use_case = container.sql.user().GetUserByKeycloakIdProvider(
        UserRepository__db=db
    )
    try:
        user = get_user_use_case.execute(keycloak_user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------- UPDATE --------------------
@router.put("/{user_id}")
async def update_user_by_id(
    user_id: uuid.UUID,
    new_user: UpdateUserDTO,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    update_user_use_case = container.sql.user().UpdateUserByIdProvider(
        UserRepository__db=db,
        event_repository=event_repo,
    )
    try:
        updated = await update_user_use_case.execute(user_id, new_user)
        if updated:
            return {"message": "User updated successfully"}
        raise HTTPException(status_code=400, detail="User update failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------- DELETE --------------------
@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    container: Container = request.app.state.container
    event_repo = container.NoSQL.events().EventRepositoryProvider()
    delete_user_use_case = container.sql.user().DeleteUserByIdProvider(
        UserRepository__db=db,
        event_repository=event_repo,
    )
    try:
        deleted = await delete_user_use_case.execute(user_id)
        if deleted:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))