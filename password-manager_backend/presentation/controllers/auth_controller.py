from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class TokenRequest(BaseModel):
    code: str

class TokenResponse(BaseModel):
    token: str

@router.post("/auth/token", response_model=TokenResponse)
async def exchange_code_for_token(request: TokenRequest):
    """
    Scambia il codice di autorizzazione di Keycloak con un token JWT
    """
    try:
        # Configurazione Keycloak dalle variabili d'ambiente
        keycloak_host = os.getenv("KEYCLOAK_HOST")
        keycloak_port = os.getenv("KEYCLOAK_PORT")
        keycloak_url = f"http://{keycloak_host}:{keycloak_port}"
        realm = os.getenv("KEYCLOAK_REALM")
        client_id = os.getenv("KEYCLOAK_CLIENT_ID")
        client_secret = os.getenv("KEYCLOAK_SECRET")

        print(f"Configurazione Keycloak: host={keycloak_host}, port={keycloak_port}, realm={realm}, client_id={client_id}")
        print(f"Client secret presente: {bool(client_secret)}")

        # URL per lo scambio del token
        token_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/token"
        print(f"Token URL: {token_url}")

        # Dati per la richiesta - NON includere client_secret per client public
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": request.code,
            "redirect_uri": "http://localhost:3000/auth/callback"
        }

        print(f"Dati richiesta: {data}")

        # Richiesta a Keycloak
        async with httpx.AsyncClient() as client:
            response = await client.post(
                token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            print(f"Risposta Keycloak: status={response.status_code}, body={response.text}")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Errore da Keycloak: {response.text}"
                )

            token_data = response.json()
            print(f"Token ricevuto: {bool(token_data.get('access_token'))}")

            # Restituisci il token di accesso
            return TokenResponse(token=token_data.get("access_token"))

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore di connessione a Keycloak: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore interno: {str(e)}"
        )
