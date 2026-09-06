import os
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import requests

KEYCLOAK_HOST = os.getenv("KEYCLOAK_HOST")
KEYCLOAK_PORT = os.getenv("KEYCLOAK_PORT")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE")

KEYCLOAK_BASE = f"http://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}/realms/{KEYCLOAK_REALM}"

# FastAPI uses this to pull the token out of the Authorization header.
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/token",
    refreshUrl=f"{KEYCLOAK_BASE}/protocol/openid-connect/token",
    scopes={
        "openid": "OpenID Connect scope",
        "profile": "User profile information",
        "email": "User email address",
    },
)


def get_keycloak_public_keys():
    response = requests.get(f"{KEYCLOAK_BASE}/protocol/openid-connect/certs")
    return response.json()


async def jwt_authentication(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    """Verifies the bearer token against Keycloak and returns its payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # ponytail: fetches Keycloak's JWKS on every request, no cache.
        # Fine at current traffic; add an lru_cache/TTL cache if Keycloak
        # calls per-request become a bottleneck.
        jwks = get_keycloak_public_keys()

        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=KEYCLOAK_AUDIENCE,
            issuer=KEYCLOAK_BASE,
        )

        if payload.get("sub") is None:
            raise credentials_exception

    except JWTError as e:
        raise credentials_exception from e

    return payload
