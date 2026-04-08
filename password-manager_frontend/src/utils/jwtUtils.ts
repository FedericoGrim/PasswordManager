/**
 * Decodifica un JWT token e estrae i dati (payload)
 */
export interface JWTPayload {
  sub: string;
  email?: string;
  name?: string;
  preferred_username?: string;
  email_verified?: boolean;
  realm_access?: {
    roles: string[];
  };
  [key: string]: any;
}

export const decodeJWT = (token: string): JWTPayload | null => {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) {
      console.error("Token JWT non valido");
      return null;
    }

    // Decodifica il payload (seconda parte)
    const payload = parts[1];
    const decodedPayload = atob(payload);
    const parsedPayload = JSON.parse(decodedPayload);

    return parsedPayload;
  } catch (error) {
    console.error("Errore nella decodifica del JWT:", error);
    return null;
  }
};

/**
 * Estrae il `sub` dal JWT token
 */
export const extractSubFromToken = (token: string): string | null => {
  const payload = decodeJWT(token);
  return payload?.sub || null;
};
