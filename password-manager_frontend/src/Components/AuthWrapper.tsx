"use client";
import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = sessionStorage.getItem("IdToken");
    const publicRoutes = ["/auth", "/auth/callback"];

    // Se l'utente accede a una rotta privata senza token, reindirizza all'autenticazione
    if (!token && !publicRoutes.includes(pathname)) {
      router.replace("/auth");
      return;
    }

    setIsLoading(false);
  }, [pathname, router]);

  // Mostra un loading durante il controllo dell'autenticazione
  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#778da9] text-[#0d1b2a] flex items-center justify-center">
        <div className="bg-[#e0e1dd] rounded-xl shadow-lg p-8 border border-[#415a77]">
          <h1 className="text-2xl font-bold mb-2">Caricamento...</h1>
          <p className="text-[#415a77]">Verifica dell'autenticazione in corso</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
