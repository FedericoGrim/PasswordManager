"use client";

import { useEffect, useState } from "react";
import { createMainUser, getMainUserByKeycloakId, getSubAccountsByUserId, deleteSubAccount } from "../../api/apis";
import { Decrypt, DeriveKey, GenerateSalt } from "../../Functions/Cripting-Decripting/Cript-Dectipr";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";
import { UUID } from "crypto";

import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';

export default function Home() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [subAccounts, setSubAccounts] = useState<subAccount[]>([]);
  const [IsLoading, SetIsLoading] = useState(true);
  const [showMasterPassword, setShowMasterPassword] = useState(true);
  const [masterPassword, setMasterPassword] = useState("");
  const [error, setError] = useState("");
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({});
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("IdToken");
    if (!token) {
      router.replace("/login-register");
      return;
    }

    const existingKey = sessionStorage.getItem("Key");
    if (existingKey) {
      SetKeyBuffer(Buffer.from(existingKey, "hex"));
      setShowMasterPassword(false);
    }

    let keycloakId: UUID | null = null;
    try {
      const payloadBase64 = token.split(".")[1];
      const payloadJson = JSON.parse(atob(payloadBase64));
      keycloakId = payloadJson.sub ?? null;
    } catch {
      router.replace("/login-register");
      return;
    }

    (async () => {
      try {
        if (!keycloakId) {
          router.replace("/login-register");
          return;
        }

        let user = await getMainUserByKeycloakId(keycloakId);
        if (!user) {
          const salt = GenerateSalt();
          await createMainUser(keycloakId, Buffer.from(salt).toString("hex"));
          user = await getMainUserByKeycloakId(keycloakId);
        }

        if (!user?.Id) {
          router.replace("/login-register");
          return;
        }

        sessionStorage.setItem("UserId", user.Id);
        sessionStorage.setItem("Salt", user.SaltArgon);
        SetUserId(user.Id);
        SetIsLoading(false);
      } catch {
        router.replace("/login-register");
      }
    })();
  }, [router]);

  useEffect(() => {
    if (!UserId) return;
    const fetchData = async () => {
      const data = await getSubAccountsByUserId(UserId);
      if (data.length > 0) sessionStorage.setItem("subAccountData", JSON.stringify(data[0]));
      setSubAccounts(data);
    };
    fetchData();
  }, [UserId]);

  const handleMasterPasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const salt = sessionStorage.getItem("Salt");
    if (!salt) {
      setError("Salt non disponibile, ricaricare la pagina.");
      return;
    }

    try {
      const key = await DeriveKey(masterPassword, Buffer.from(salt, "utf-8"));
      sessionStorage.setItem("Key", key.toString("hex"));
      SetKeyBuffer(key);
      setShowMasterPassword(false);
      setMasterPassword("");
      setError("");
    } catch {
      setError("Errore nella derivazione della chiave. Riprova.");
    }
  };

  const HandleDeleteSubAccount = async (sa: subAccount) => {
    if (!confirm("Sei sicuro di voler eliminare questo subaccount?")) return;
    await deleteSubAccount(sa.id);
    setSubAccounts(prev => prev.filter(s => s.id !== sa.id));
  };

  const TogglePassword = (id: string) => {
    setShowPasswords(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  if (IsLoading) return <div className="text-center mt-20 text-gray-400">Caricamento...</div>;

  return (
    <div className="min-h-screen bg-[#0D1B2A] text-gray-100 flex flex-col ">
      <main className="flex-1 max-w-5xl mx-auto w-full p-6">
        {showMasterPassword && (
          <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
            <form
              onSubmit={handleMasterPasswordSubmit}
              className="bg-[#1B263B] rounded-2xl shadow-lg p-8 flex flex-col gap-4 w-[350px]"
            >
              <h2 className="text-xl font-semibold text-center text-white">Inserisci la tua Master Password</h2>
              <input
                type="password"
                value={masterPassword}
                onChange={e => setMasterPassword(e.target.value)}
                className="border border-gray-500 p-2 rounded-lg bg-[#0D1B2A] text-white focus:outline-none focus:ring-2 focus:ring-white"
                placeholder="Master Password"
                required
                autoFocus
              />
              {error && <div className="text-red-500 text-sm">{error}</div>}
              <button
                type="submit"
                className="bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition"
              >
                Sblocca
              </button>
            </form>
          </div>
        )}

        <h2 className="text-2xl font-bold mb-6 text-white">I tuoi account:</h2>

        {subAccounts.length === 0 && !showMasterPassword ? (
          <div className="text-gray-400 italic text-center mt-20">
            Nessun subaccount salvato.<br />
            <span
              className="text-white cursor-pointer hover:underline"
              onClick={() => router.push("/create-subaccount")}
            >
              Aggiungine uno ora
            </span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Card crea nuovo subaccount */}
            <div
              onClick={() => router.push("/create-subaccount")}
              className="flex flex-col items-center justify-center bg-white/10 border border-white/20 rounded-2xl p-6 shadow-lg hover:shadow-gray-500/40 transition-all backdrop-blur-md cursor-pointer text-white"
            >
              <div className="text-4xl font-bold mb-2">➕</div>
              <div className="text-lg font-semibold">Crea nuovo</div>
            </div>

            {/* Card subaccount esistenti */}
            {subAccounts.map(sa => (
              <div
                key={sa.id}
                className="bg-white/10 border border-white/20 rounded-2xl p-5 shadow-lg hover:shadow-gray-500/30 transition-all backdrop-blur-md"
              >
                <p className="text-white text-sm font-semibold">{sa.title}</p>
                <p className="mt-1 text-sm text-gray-300"><strong>👤</strong> {sa.username}</p>
                <p className="truncate text-sm mt-1 text-gray-300">
                  <strong>🔑</strong>{" "}
                  {KeyBuffer
                    ? showPasswords[sa.id]
                      ? Decrypt(sa.password, KeyBuffer)
                      : "••••••••"
                    : "Chiave non disponibile"}
                  {KeyBuffer && (
                    <button
                      type="button"
                      onClick={() => TogglePassword(sa.id)}
                      className="ml-2 text-white hover:underline text-xs"
                    >
                      {showPasswords[sa.id] ? <VisibilityOffIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
                    </button>
                  )}
                </p>

                <div className="flex gap-3 mt-4">
                  <button
                    onClick={() => router.push("/edit-subaccount")}
                    className="flex-1 bg-yellow-500 text-white py-1.5 rounded-lg hover:bg-yellow-600 transition-all shadow hover:shadow-yellow-500/30"
                  >
                    ✏️ Modifica
                  </button>
                  <button
                    onClick={() => HandleDeleteSubAccount(sa)}
                    className="flex-1 bg-red-600 text-white py-1.5 rounded-lg hover:bg-red-700 transition-all shadow hover:shadow-red-500/30"
                  >
                    🗑️ Elimina
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
