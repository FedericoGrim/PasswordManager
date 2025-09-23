"use client";
// pages/login.js
import { useEffect } from "react";

export default function LoginPage() {
  useEffect(() => {
    const keycloakUrl = new URL(
      "http://localhost:8080/realms/Test/protocol/openid-connect/auth"
    );
    keycloakUrl.searchParams.append("client_id", "password-manager-frontend");
    keycloakUrl.searchParams.append(
      "redirect_uri",
      "http://localhost:3000/home"
    );
    keycloakUrl.searchParams.append("response_type", "code");
    keycloakUrl.searchParams.append("scope", "openid");

    // Redirige subito
    window.location.href = keycloakUrl.toString();
  }, []);

  return (
    <div>
      <h1>Reindirizzamento in corso...</h1>
    </div>
  );
}
