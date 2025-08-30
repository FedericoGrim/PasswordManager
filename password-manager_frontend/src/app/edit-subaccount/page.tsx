"use client";

import { useEffect, useState } from "react";
import { 
  updateSubAccount
} from "../../api/apis";
import { UUID } from "crypto";

import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";

export default function EditSubAccountPage() {
  const [subAcc, setSubAcc] = useState<subAccount | null>(null);
  const [userId, setUserId] = useState<UUID | null>(null);
  const [salt, setSalt] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const storedDatas = sessionStorage.getItem("subAccountData");
    const storedUserId = sessionStorage.getItem("UserId");
    const storedUserSalt = sessionStorage.getItem("userSalt");
    console.log("subAccountData:", storedDatas);
    console.log("UserId:", storedUserId);
    console.log("userSalt:", storedUserSalt);
    if (storedDatas) setSubAcc(JSON.parse(storedDatas));
    if (storedUserId) setUserId(storedUserId as UUID);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!subAcc) return;
    setSubAcc({ ...subAcc, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    if (!subAcc || !userId || !salt) return;
    await updateSubAccount(subAcc, userId, salt); // aggiungi user_id
    alert("Modifiche salvate!");
    router.push("/");
  };

  if (!subAcc) return <div>Caricamento dati...</div>;

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-6">Modifica Subaccount</h1>
      <form className="flex flex-col gap-4" onSubmit={e => { e.preventDefault(); handleSave(); }}>
        <label>
          Titolo:
          <input
            type="text"
            name="title"
            value={subAcc.title}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
          />
        </label>
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={subAcc.username}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
          />
        </label>
        <label>
          URL:
          <input
            type="text"
            name="url"
            value={subAcc.url}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
          />
        </label>
        <label>
          Password:
          <input
            type="text"
            name="password_encrypted"
            value={subAcc.password_encrypted ?? ""}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
          />
        </label>
        <button
          type="submit"
          className="px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700"
        >
          Salva modifiche
        </button>
      </form>
    </div>
  );
}
