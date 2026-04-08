import axios from 'axios';
import keycloak from './keycloakClient'; // L'istanza esportata sopra

const axiosClient = axios.create({
    baseURL: 'http://localhost:8000',
});

axiosClient.interceptors.request.use(
    async (config) => {
        const sessionToken = typeof window !== 'undefined' ? sessionStorage.getItem('IdToken') : null;
        if (sessionToken) {
            config.headers.Authorization = `Bearer ${sessionToken}`;
            return config;
        }

        if (keycloak) {
            try {
                // Rinfresca se il token scade entro 30 secondi
                await keycloak.updateToken(30);
                const token = keycloak.token;
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
            } catch (error) {
                console.error("Token refresh failed", error);
                keycloak.login(); // Forza il re-login se la sessione è scaduta del tutto
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosClient;