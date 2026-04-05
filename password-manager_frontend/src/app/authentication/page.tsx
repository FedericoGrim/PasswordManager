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

    const keycloakUrl = process.env.NEXT_PUBLIC_KEYCLOAK_URL;
    const realm = process.env.NEXT_PUBLIC_KEYCLOAK_REALM;
    const clientId = process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID;

    const KeycloakUrl = new URL(
      `${keycloakUrl}/realms/${realm}/protocol/openid-connect/auth`
    );
    KeycloakUrl.searchParams.append("client_id", clientId || "");
    KeycloakUrl.searchParams.append(
      "redirect_uri",
      "http://localhost:3000/auth/callback"
    );
    KeycloakUrl.searchParams.append("response_type", "code");
    KeycloakUrl.searchParams.append("scope", "openid");

    window.location.href = KeycloakUrl.toString();
  }, [router]);

  return (
    <div className="min-h-screen bg-[#778da9] text-[#0d1b2a] flex items-center justify-center">
      <div className="bg-[#e0e1dd] rounded-xl shadow-lg p-8 border border-[#415a77]">
        <h1 className="text-2xl font-bold mb-2">
          Reindirizzamento a Keycloak...
        </h1>
        <p className="text-[#415a77]">Attendi qualche secondo</p>
      </div>
    </div>
  );
}
