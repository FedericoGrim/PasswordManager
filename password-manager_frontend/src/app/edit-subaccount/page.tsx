"use client";

import { useEffect, useState } from "react";
import { updateSubAccount } from "../../api/apis";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";
import { Decrypt, DeriveKey, Encrypt } from "../../Functions/Cripting-Decripting/Cript-Dectipr";

export default function EditSubAccountPage() {
  const [subAcc, setSubAcc] = useState<subAccount | null>(null);
  const [salt, setSalt] = useState<string | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const storedDatas = sessionStorage.getItem("subAccountData");
    const storedUserSalt = sessionStorage.getItem("Salt");
    const storedUserKey = sessionStorage.getItem("Key");

    if (storedDatas && storedUserSalt && storedUserKey) {
      try {
        const parsedSubAcc: subAccount = JSON.parse(storedDatas);

        // Usa la chiave già derivata e salvata in sessionStorage
        const buf = Buffer.from(storedUserKey.match(/.{1,2}/g)!.map(b => parseInt(b, 16)));
        parsedSubAcc.password = Decrypt(parsedSubAcc.password, buf);

        setSubAcc(parsedSubAcc);
        setSalt(storedUserSalt);
        SetKeyBuffer(buf);
      } catch (error) {
        console.error("Errore nel parsing o decrypt:", error);
      }
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!subAcc) return;
    const { name, value } = e.target;
    setSubAcc(prev => prev ? { ...prev, [name]: value } : prev);
  };

  const handleSave = async () => {
    if (!subAcc || !salt || !KeyBuffer) {
      alert("Chiave o dati mancanti. Impossibile salvare.");
      return;
    }

    try {
      const updatedSubAcc: subAccount = {
        ...subAcc,
        password: Encrypt(subAcc.password, KeyBuffer)
      };

      await updateSubAccount(updatedSubAcc, updatedSubAcc.id);
      alert("Modifiche salvate!");
      router.push("/home");
    } catch (error) {
      console.error("Errore nel salvataggio:", error);
      alert("Errore durante il salvataggio");
    }
  };

  if (!subAcc) return <div>Caricamento dati...</div>;

  return (
    <div className="min-h-screen bg-[#415a77] text-[#e0e1dd] p-6 flex items-center justify-center">
      <div className="max-w-lg w-full bg-[#1b263b] rounded-xl shadow-lg p-8 border border-[#778da9]">
        <h1 className="text-2xl font-bold mb-6 text-[#e0e1dd]">Modifica Subaccount</h1>
        <form
          className="flex flex-col gap-4"
          onSubmit={e => { e.preventDefault(); handleSave(); }}
        >
          {["title", "username", "url"].map(field => (
            <label key={field}>
              {field.charAt(0).toUpperCase() + field.slice(1)}:
              <input
                type="text"
                name={field}
                value={subAcc[field as keyof subAccount] as string}
                onChange={handleChange}
                className="border rounded px-2 py-1 w-full"
              />
            </label>
          ))}
          <label>
            Password:
            <div className="flex items-center gap-2">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={subAcc.password}
                onChange={handleChange}
                className="border rounded px-2 py-1 w-full"
              />
              <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                className="px-2 py-1 bg-gray-300 rounded hover:bg-gray-400"
              >
                {showPassword ? "Nascondi" : "Mostra"}
              </button>
            </div>
          </label>
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700"
          >
            Salva modifiche
          </button>
        </form>
      </div>
    </div>
  );
}
