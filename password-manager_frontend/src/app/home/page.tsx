"use client";

import { useEffect, useState } from "react";
import { createMainUser, getMainUserByKeycloakId, getSubAccountsByUserId, deleteSubAccount } from "../../api/apis";
import { Decrypt, DeriveKey, GenerateSalt } from "../crypto/decript";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";
import { UUID } from "crypto";

export default function ProfilePage() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [subAccounts, setSubAccounts] = useState<subAccount[]>([]);
  const [IsLoading, SetIsLoading] = useState(true);
  const [showMasterPassword, setShowMasterPassword] = useState(true);
  const [masterPassword, setMasterPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("IdToken");
    if (!token) {
      router.replace("/login-register");
      return;
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

  if (IsLoading) return <div>Caricamento...</div>;

  return (
    <div className="p-6">
      {showMasterPassword && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <form
            onSubmit={handleMasterPasswordSubmit}
            className="bg-white rounded-lg shadow-lg p-8 flex flex-col gap-4 min-w-[320px]"
          >
            <h2 className="text-lg font-bold">Inserisci la tua Master Password</h2>
            <input
              type="password"
              value={masterPassword}
              onChange={e => setMasterPassword(e.target.value)}
              className="border p-2 rounded"
              placeholder="Master Password"
              required
              autoFocus
            />
            {error && <div className="text-red-600">{error}</div>}
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Sblocca
            </button>
          </form>
        </div>
      )}

      <div className="flex justify-between items-center mb-4">
        <button
          onClick={() => router.push("/create-subaccount")}
          className="px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700"
        >
          ➕ Crea subaccount
        </button>
      </div>

      <h2 className="text-lg font-semibold mb-4">I tuoi sottoaccount:</h2>
      {subAccounts.length === 0 ? (
        <div className="text-gray-600 italic mb-4">Nessun subaccount registrato</div>
      ) : (
        <ul className="space-y-4">
          {subAccounts.map(sa => (
            <li
              key={sa.id}
              className="p-4 rounded-2xl shadow-md border bg-[#0A9396] flex flex-col gap-2 text-[#001219]"
            >
              <p><strong>Title:</strong> {sa.title}</p>
              <p><strong>Username:</strong> {sa.username}</p>
              <p>
                <strong>Password:</strong>{" "}
                {KeyBuffer ? Decrypt(sa.password, KeyBuffer) : "Chiave non disponibile"}
              </p>
              <div className="flex gap-4 mt-2">
                <button
                  onClick={() => router.push("/edit-subaccount")}
                  className="px-3 py-1 bg-yellow-500 text-white rounded-lg shadow hover:bg-yellow-600"
                >
                  ✏️ Modifica
                </button>
                <button
                  onClick={() => HandleDeleteSubAccount(sa)}
                  className="px-3 py-1 bg-red-600 text-white rounded-lg shadow hover:bg-red-700"
                >
                  🗑️ Elimina
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
