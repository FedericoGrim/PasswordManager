"use client";

import { useEffect, useState } from "react";
import { getSubAccountsByUserId, deleteSubAccount } from "../../api/apis";
import { Decrypt } from "../crypto/decript";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";
import { UUID } from "crypto";

export default function ProfilePage() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [subAccounts, setSubAccounts] = useState<subAccount[]>([]);
  const router = useRouter();

  useEffect(() => {
    const Id = sessionStorage.getItem("UserId") as UUID | null;
    const KeyRaw = sessionStorage.getItem("Key");
    console.log("Retrieved Key from sessionStorage:", KeyRaw);

    SetUserId(Id);

    if (KeyRaw) {
      const Buf = Buffer.from(
        KeyRaw.match(/.{1,2}/g)!.map(b => parseInt(b, 16))
      );
      SetKeyBuffer(Buf);
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (UserId) {
        const data = await getSubAccountsByUserId(UserId);

        // Salva nel sessionStorage il primo subaccount (o quello che vuoi modificare)
        if (data.length > 0) {
          sessionStorage.setItem("subAccountData", JSON.stringify(data[0]));
        }

        setSubAccounts(data);
      }
    };
    fetchData();
  }, [UserId]);

  const [IsLoading, SetIsLoading] = useState(true);

  useEffect(() => {
    const Id = sessionStorage.getItem("UserId") as UUID | null;
    const KeyRaw = sessionStorage.getItem("Key");

    SetUserId(Id);

    if (KeyRaw) {
      const Buf = Buffer.from(
        KeyRaw.match(/.{1,2}/g)!.map(b => parseInt(b, 16))
      );
      SetKeyBuffer(Buf);
    }

    SetIsLoading(false); // lettura completata
  }, []);

  useEffect(() => {
    if (!IsLoading && !UserId) {
      router.push("/login-singin");
    }
  }, [IsLoading, UserId, router]);

  const HandleDeleteSubAccount = async (sa: subAccount) => {
    if (!confirm("Sei sicuro di voler eliminare questo subaccount?")) return;
    await deleteSubAccount(sa.id);
    setSubAccounts(prev => prev.filter(s => s.id !== sa.id));
  };

  return (
    <div className="p-6">
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
            <li key={sa.id} className="p-4 rounded-2xl shadow-md border bg-[#0A9396] flex flex-col gap-2 text-[#001219]">
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
