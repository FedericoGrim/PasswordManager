# Keyden — Backend

FastAPI service for Keyden. See the [root README](../readme.md) for the full-stack overview, architecture, and encryption model.

## Running locally

Requires the dev database + Keycloak stack to be running first (`docker compose -f ../SDK/develop/docker-compose.yml up -d`) and a `.env` file (copy `.env.example` and fill in the values).

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --app-dir src
```

`main.py` lives in `src/`, so `--app-dir src` is required — running plain `uvicorn main:app` from this folder will fail with a module-not-found error.

## API docs

Once the server is running:

- Swagger UI — http://localhost:8000/docs
- ReDoc — http://localhost:8000/redoc

## Other guides

- [Database migrations](migrations/README)
- [Tests](tests/Readme.md)
- [Sphinx code docs](docs/readme.md)
