# Keyden — Frontend

Next.js (App Router) client for Keyden. See the [root README](../readme.md) for the full-stack overview, architecture, and encryption model.

All password encryption/decryption and key wrapping happens in this app, in the browser — see [`src/Functions/Cripting-Decripting`](src/Functions/Cripting-Decripting) and [`src/Functions/Provisioning`](src/Functions/Provisioning).

## Running locally

Requires the backend API and Keycloak to be running (see the root README).

```bash
npm install
npm run dev
```

Open http://localhost:3000.

### Environment variables

Read from `NEXT_PUBLIC_*` (see [`src/api/envVars.ts`](src/api/envVars.ts)):

| Variable | Purpose |
|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL of the Keyden backend API |
| `NEXT_PUBLIC_KEYCLOAK_URL` | Keycloak server URL |
| `NEXT_PUBLIC_KEYCLOAK_REALM` | Keycloak realm (`PasswordManager` in the dev stack) |
| `NEXT_PUBLIC_KEYCLOAK_CLIENT_ID` | Keycloak client ID |
| `NEXT_PUBLIC_KEYCLOAK_REFRESH_INTERVAL` | Token refresh interval, in seconds |

## Scripts

- `npm run dev` — start the dev server (Turbopack)
- `npm run build` — production build
- `npm run start` — run a production build
- `npm run lint` — run ESLint

## Structure

```
src/app/                       routes (App Router): auth, home, teams, settings
src/Components/                shared UI (Sidebar, Footer, AuthGate, ...)
src/Functions/Cripting-Decripting/  client-side crypto (Argon2id, AES-GCM, ECDH/ML-KEM hybrid wrap)
src/Functions/Provisioning/    user & team-key provisioning flows
src/api/                       axios client, Keycloak client, entity types
```
