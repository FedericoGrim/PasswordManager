"use client";
import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { extractSubFromToken } from "@/utils/jwtUtils";
import { createMainUser, getMainUserByKeycloakId } from "@/api/apis";

export default function CallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const exchangeCodeForToken = async () => {
      try {
        const code = searchParams.get("code");
        const state = searchParams.get("state");

        if (!code) {
          console.error("Nessun codice ricevuto da Keycloak");
          router.replace("/auth");
          return;
        }

        // Invia il codice al backend per scambiarlo con il token
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/token`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              code: code,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Errore nello scambio del codice con il token");
        }

        const data = await response.json();

        // Memorizza il token in sessionStorage
        if (data.token || data.IdToken) {
          const token = data.token || data.IdToken;
          sessionStorage.setItem("IdToken", token);

          // Estrai il sub dal token
          const sub = extractSubFromToken(token);
          if (sub) {
            sessionStorage.setItem("keycloakId", sub);

            try {
              const existingUser = await getMainUserByKeycloakId(sub);
              if (existingUser) {
                console.log("Utente già presente nel backend", existingUser);
              } else {
                await createMainUser(sub);
                console.log("Utente creato con successo nel backend");
              }
            } catch (error) {
              console.error("Errore durante il controllo / creazione dell'utente:", error);
              alert("Autenticazione completata ma si è verificato un problema nella verifica del profilo utente");
            }
          }

          router.replace("/home");
        } else {
          console.error("Token non ricevuto dal backend");
          router.replace("/auth");
        }
      } catch (error) {
        console.error("Errore durante il callback:", error);
        router.replace("/auth");
      }
    };

    exchangeCodeForToken();
  }, [searchParams, router]);

  return (
    <div className="min-h-screen bg-[#778da9] text-[#0d1b2a] flex items-center justify-center">
      <div className="bg-[#e0e1dd] rounded-xl shadow-lg p-8 border border-[#415a77]">
        <h1 className="text-2xl font-bold mb-2">Completamento autenticazione...</h1>
        <p className="text-[#415a77]">Salvataggio del token in corso</p>
      </div>
    </div>
  );
}
