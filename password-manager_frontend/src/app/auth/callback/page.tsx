"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AuthCallback() {
  const router = useRouter();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      fetch("http://localhost:8080/realms/PasswordManager/protocol/openid-connect/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "authorization_code",
          client_id: "PasswordManager-frontend",
          code,
          redirect_uri: "http://localhost:3000/auth/callback",
        }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.id_token) {
            sessionStorage.setItem("IdToken", data.id_token);
            router.replace("/home");
          } else {
            alert("Errore autenticazione");
            router.replace("/login");
          }
        });
    } else {
      router.replace("/login-register");
    }
  }, [router]);

  return <div>Autenticazione in corso...</div>;
}