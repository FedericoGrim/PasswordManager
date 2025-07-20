import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from uuid import UUID
from dependency_injector.wiring import inject

from config import Container
from Application.DTO.LocalUserDTO import CreateLocalUser, UpdateLocalUser
from Infrastructure.Repositories.Database import get_db

routerV1 = APIRouter()

@routerV1.post("/")
@inject
async def ApiCreateUser(
    localUser: CreateLocalUser, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    """
    Crea un nuovo utente locale nel database.

    Args:
        localUser (CreateLocalUser): DTO contenente i dati per creare l'utente.
        db (Session): Sessione di database fornita da FastAPI tramite Depends.
        request (Request, opzionale): Oggetto request per accedere al container di dipendenze.

    Returns:
        dict: Messaggio di conferma e dati utente creato.

    Raises:
        HTTPException: Errore con status 400 in caso di fallimento.
    """

    container: Container = request.app.container

    create_user_use_case = container.local_user().CreateLocalUserProvider(LocalUserRepository__db=db)

    try:
        created_user = create_user_use_case.execute(localUser)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@routerV1.get("/{keycloak_user_id}")
@inject
async def ApiGetUser(
    keycloak_user_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    """
    Recupera un utente locale tramite il suo ID Keycloak.

    Args:
        keycloakUserId (UUID): Identificativo univoco dell'utente Keycloak.
        db (Session): Sessione di database fornita da FastAPI.
        request (Request, opzionale): Oggetto request per il container DI.

    Returns:
        dict: Messaggio di conferma e dati utente recuperato.

    Raises:
        HTTPException: Errore 404 se l'utente non è trovato.
    """
    container: Container = request.app.container
    get_user_use_case = container.local_user().GetAllLocalUsersByMainUserIdProvider(LocalUserRepository__db=db)
    
    try:
        user = get_user_use_case.execute(keycloak_user_id)
        return {"message": "User retrieved successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@routerV1.put("/{user_id}")
@inject
async def ApiUpdateLocalUser(
    localUserId: UUID, 
    salt: str, 
    newLocalUser: UpdateLocalUser,
    db: Session = Depends(get_db), 
    request: Request = None
):
    """
    Aggiorna i dati di un utente locale specificato dall'ID.

    Args:
        localUserId (UUID): ID univoco dell'utente locale da aggiornare.
        salt (str): Valore salt usato per l'hashing della password.
        newLocalUser (UpdateLocalUser): DTO con i nuovi dati utente.
        db (Session): Sessione database.
        request (Request, opzionale): Oggetto request per container DI.

    Returns:
        dict: Messaggio di conferma aggiornamento.

    Raises:
        HTTPException: Errore 400 in caso di problemi durante l'aggiornamento.
    """
    container: Container = request.app.container
    update_user_username_use_case = container.local_user().UpdateLocalUserByIdProvider(LocalUserRepository__db=db)
    
    try:
        user_username_updated = update_user_username_use_case.execute(localUserId, newLocalUser, salt)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@routerV1.delete("/{user_id}")
@inject
async def ApiDeleteUser(
    localUserId: UUID, 
    db: Session = Depends(get_db), 
    request: Request = None
):
    """
    Elimina un utente locale dal database.

    Args:
        localUserId (UUID): ID dell'utente da eliminare.
        db (Session): Sessione database.
        request (Request, opzionale): Oggetto request per container DI.

    Returns:
        dict: Messaggio di conferma eliminazione.

    Raises:
        HTTPException: Errore 400 se l'eliminazione fallisce.
    """
    container: Container = request.app.container
    delete_user_use_case = container.local_user().DeleteLocalUserByIdProvider(LocalUserRepository__db=db)
    
    try:
        if delete_user_use_case.execute(localUserId):
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="User deletion failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
