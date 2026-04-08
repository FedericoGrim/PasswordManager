import Keycloak from 'keycloak-js';
import { getEnvVar } from './envVars';

let keycloak: Keycloak | null = null;

const keycloakFactory = (): Keycloak => {
  if (!keycloak) {
    const keycloakUrl = getEnvVar('KEYCLOAK_URL', process.env.NEXT_PUBLIC_KEYCLOAK_URL);
    const keycloakRealm = getEnvVar('KEYCLOAK_REALM', process.env.NEXT_PUBLIC_KEYCLOAK_REALM);
    const keycloakClientId = getEnvVar('KEYCLOAK_CLIENT_ID', process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID);

    keycloak = new Keycloak({
      url: keycloakUrl,
      realm: keycloakRealm,
      clientId: keycloakClientId
    });

    keycloak.init({ 
      onLoad: 'login-required',
      pkceMethod: 'S256' // Coerenza con la config del backend/Swagger
    }).then((authenticated) => {
      if (authenticated) {
        console.log('Keycloak authenticated');
      }
    }).catch(err => console.error('Keycloak init error', err));
  }
  return keycloak;
};

const hasRoleAccess = (role: string): boolean => {
  return keycloak?.tokenParsed?.['extranet-roles']?.includes(role) || false;
};

// Esportiamo l'istanza factory
export { keycloakFactory, hasRoleAccess };
// Esportiamo anche l'oggetto singleton per l'interceptor
export default keycloakFactory();