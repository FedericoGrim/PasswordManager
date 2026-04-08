import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import requests
from sqlalchemy.orm import Session
# Importa i tuoi modelli e la logica DB
from infrastructure.databases.sql.database import get_db 
from domain.entities.user import User # Il tuo modello SQLAlchemy

# Configurazione (meglio se letta da .env via config.py)
KEYCLOAK_HOST = os.getenv("KEYCLOAK_HOST") # es. https://auth.tuodominio.it
KEYCLOAK_PORT = os.getenv("KEYCLOAK_PORT")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
AUDIENCE = os.getenv("KEYCLOAK_CLIENT_ID")

# Endpoint per recuperare le chiavi pubbliche di Keycloak
KEYCLOAK_BASE = f"http://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}/realms/{KEYCLOAK_REALM}"

# FastAPI userà questo per estrarre il token dall'header Authorization
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/token",
    refreshUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/token",
    scopes={"openid": "OpenID Connect scope",
            "profile": "User profile information",
            "email": "User email address"}
)

def get_keycloak_public_keys():
    """Recupera le chiavi pubbliche da Keycloak per validare la firma del JWT"""
    response = requests.get(f"{KEYCLOAK_BASE}/protocol/openid-connect/certs")
    return response.json()

async def jwt_authentication(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Verifica il token e restituisce l'utente dal database locale.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token non valido o scaduto",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Recupera le chiavi (In produzione: usa una cache per non chiamare Keycloak ogni volta!)
        jwks = get_keycloak_public_keys()
        
        # 2. Decodifica e valida il JWT
        # Nota: 'jwt.decode' verifica firma, scadenza (exp) e audience
        # In jwt_token_autentication.py

        # Usa KEYCLOAK_BASE che ha già http://
        payload = jwt.decode(
            token, 
            jwks, 
            algorithms=["RS256"], 
            audience=AUDIENCE,
            issuer=KEYCLOAK_BASE # <--- Molto più sicuro così
        )
        
        # 3. Estrai l'ID univoco di Keycloak (sub)
        keycloak_id: str | None = payload.get("sub")
        if keycloak_id is None:
            raise credentials_exception

    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception

    # 4. Cerca l'utente nel tuo Database locale
    # Assumiamo che nel tuo modello User ci sia un campo 'keycloak_id'
    user = db.query(User).filter(User.keycloak_id == keycloak_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente autenticato ma non presente nel database locale"
        )

    return user