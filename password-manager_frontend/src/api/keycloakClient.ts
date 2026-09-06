import Keycloak from 'keycloak-js';
import axiosClient from './axiosClient';
import { getEnvVar, getIntEnvVar } from './envVars';

let keycloak: Keycloak | null = null;

const logTokenDetails = (tokenParsed: any) => {
  if (tokenParsed) {
    console.log(`Token details:
      exp: ${tokenParsed.exp}
      iat: ${tokenParsed.iat}
      jti: ${tokenParsed.jti}
      token: ${keycloak?.token}
      ...other details: ${JSON.stringify(tokenParsed)}
    `);
  } else {
    console.log('No token details available.');
  }
};

const refreshKeycloakToken = async () => {
  if (keycloak) {
    try {
      const refreshed = await keycloak.updateToken(60);
      if (refreshed) {
        logTokenDetails(keycloak.tokenParsed);
      }
    } catch (error) {
      console.error('Failed to refresh token:', error);
      keycloak?.logout();
    }
  }
};

axiosClient.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${keycloak?.token}`;
  return config;
});

const keycloakFactory = (): Keycloak => {
  if (!keycloak) {
    var keycloakUrl = getEnvVar('KEYCLOAK_URL', process.env.NEXT_PUBLIC_KEYCLOAK_URL);
    var keycloakRealm = getEnvVar('KEYCLOAK_REALM', process.env.NEXT_PUBLIC_KEYCLOAK_REALM);
    var keycloakClientId = getEnvVar('KEYCLOAK_CLIENT_ID', process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID);
    var refreshInterval = getIntEnvVar('KEYCLOAK_REFRESH_INTERVAL', process.env.NEXT_PUBLIC_KEYCLOAK_REFRESH_INTERVAL);

    keycloak = new Keycloak({
      url: keycloakUrl,
      realm: keycloakRealm,
      clientId: keycloakClientId
    });

    // checkLoginIframe relies on a 3rd-party-cookie session check that this
    // embedded/sandboxed browser blocks (net::ERR_ABORTED on the iframe init) —
    // that false-positive "session changed" signal was forcing re-auth and
    // wiping the in-memory vault on what looked like ordinary navigation.
    keycloak.init({ onLoad: 'login-required', checkLoginIframe: false }).then((authenticated) => {
      if (authenticated) {
        logTokenDetails(keycloak?.tokenParsed);
        setInterval(refreshKeycloakToken, refreshInterval); 
      }
    });
  }
  return keycloak;
};

const hasRoleAccess = (role: string): boolean => {
  return keycloak?.tokenParsed?.['extranet-roles']?.includes(role) || false;
};

export { keycloakFactory, hasRoleAccess };