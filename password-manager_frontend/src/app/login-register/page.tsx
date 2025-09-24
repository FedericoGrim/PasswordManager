"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("IdToken");
    if (token) {
      router.replace("/home");
      return;
    }

    const KeycloakUrl = new URL(
      "http://localhost:8080/realms/PasswordManager/protocol/openid-connect/auth"
    );
    KeycloakUrl.searchParams.append("client_id", "PasswordManager-frontend");
    KeycloakUrl.searchParams.append(
      "redirect_uri",
      "http://localhost:3000/auth/callback"
    );
    KeycloakUrl.searchParams.append("response_type", "code");
    KeycloakUrl.searchParams.append("scope", "openid");

    window.location.href = KeycloakUrl.toString();
  }, [router]);

  return <h1>Reindirizzamento a Keycloak...</h1>;
}
