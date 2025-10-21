"use client";

import { useEffect, useState } from "react";
import { updateSubAccount, getSubAccountsByUserId } from "../../api/apis";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter, useSearchParams } from "next/navigation";
import { Decrypt, Encrypt } from "../../Functions/Cripting-Decripting/Cript-Dectipr";

import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import CasinoIcon from "@mui/icons-material/Casino";
import LinkIcon from '@mui/icons-material/Link';

import { UUID } from "crypto";

export default function EditSubAccountPage() {
  const [subAcc, setSubAcc] = useState<subAccount | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [passwordLength, setPasswordLength] = useState(12);
  const router = useRouter();
  const searchParams = useSearchParams();
  const SubAccountId = searchParams.get("id");

  useEffect(() => {
    const loadSubAccount = async () => {
      const storedKey = sessionStorage.getItem("Key");
      if (!storedKey) {
        alert("Chiave utente mancante. Torna alla Home e sblocca la master password.");
        router.push("/home");
        return;
      }

      const buf = Buffer.from(storedKey.match(/.{1,2}/g)!.map(b => parseInt(b, 16)));
      SetKeyBuffer(buf);

      if (!SubAccountId) {
        alert("ID subaccount mancante. Torna alla Home.");
        router.push("/home");
        return;
      }

      try {
        const userId = sessionStorage.getItem("UserId");
        if (!userId) throw new Error("UserId non disponibile");

        const subAccountsArray = await getSubAccountsByUserId(userId as unknown as UUID);
        const fetched = subAccountsArray.find(sa => sa.id === SubAccountId);
        if (!fetched) throw new Error("Subaccount non trovato");

        fetched.password = Decrypt(fetched.password, buf);
        setSubAcc(fetched);
      } catch (err) {
        console.error(err);
        alert("Impossibile caricare il subaccount. Torna alla Home.");
        router.push("/home");
      }
    };

    loadSubAccount();
  }, [SubAccountId, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!subAcc) return;
    const { name, value } = e.target;
    setSubAcc(prev => prev ? { ...prev, [name]: value } : prev);
  };

  const handleSave = async () => {
    if (!subAcc || !KeyBuffer) {
      alert("Chiave o dati mancanti. Impossibile salvare.");
      return;
    }

    try {
      const updated: subAccount = {
        ...subAcc,
        password: Encrypt(subAcc.password, KeyBuffer)
      };
      await updateSubAccount(updated, updated.id);
      alert("Modifiche salvate!");
      router.push("/home");
    } catch (err) {
      console.error(err);
      alert("Errore durante il salvataggio");
    }
  };

  const GenerateRandomPassword = (length: number) => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#@!";
    let password = "";
    for (let i = 0; i < length; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    if (subAcc) setSubAcc({ ...subAcc, password });
  };

  if (!subAcc) return <div className="text-white text-center mt-20">Caricamento dati...</div>;

  return (
    <div className="min-h-screen bg-[#0D1B2A] flex items-center justify-center p-6">
      <div className="max-w-lg w-full bg-[#1B263B]/90 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20 text-white">
        <h1 className="text-2xl font-bold mb-6 text-center">Modifica Subaccount</h1>

        <form className="flex flex-col gap-4" onSubmit={e => { e.preventDefault(); handleSave(); }}>
          {["title", "username", "url"].map(field => (
          <div key={field} className="flex flex-col">
            <label className="text-sm font-medium mb-1 capitalize">{field}</label>

            {field === "url" ? (
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  name={field}
                  value={subAcc[field as keyof subAccount] as string || ""}
                  onChange={handleChange}
                  className="flex-1 rounded-lg px-3 py-2 bg-[#0D1B2A] border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <button
                  type="button"
                  onClick={() => {
                    const url = subAcc.url?.trim();
                    if (!url) return alert("Nessun URL inserito");
                    const formattedUrl = url.startsWith("http://") || url.startsWith("https://") ? url : `https://${url}`;
                    window.open(formattedUrl, "_blank");
                  }}
                  className="px-3 py-2 bg-[#243447] rounded-lg hover:bg-[#2c3e50] transition border border-gray-500 text-sm font-semibold"
                  title="Apri link"
                >
                  <LinkIcon></LinkIcon>
                </button>
              </div>
            ) : (
              <input
                type="text"
                name={field}
                value={subAcc[field as keyof subAccount] as string || ""}
                onChange={handleChange}
                className="w-full rounded-lg px-3 py-2 bg-[#0D1B2A] border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            )}
          </div>
        ))}


          <div className="flex flex-col">
            <label className="text-sm font-medium mb-1">Password</label>
            <div className="flex items-center gap-2">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={subAcc.password || ""}
                onChange={handleChange}
                className="flex-1 rounded-lg px-3 py-2 bg-[#0D1B2A] border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                className="p-2 bg-[#243447] rounded-lg hover:bg-[#2c3e50] transition border border-gray-500"
              >
                {showPassword ? <VisibilityOffIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
              </button>
              <input
                type="number"
                min={4}
                max={64}
                value={passwordLength}
                onChange={e => setPasswordLength(Number(e.target.value))}
                className="w-16 text-white rounded-lg px-2 py-1 border border-gray-500"
                title="Lunghezza password"
              />
              <button
                type="button"
                onClick={() => GenerateRandomPassword(passwordLength)}
                className="p-2 bg-[#243447] rounded-lg hover:bg-[#2c3e50] transition text-white text-sm font-semibold border border-gray-500"
              >
                <CasinoIcon />
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="mt-4 bg-green-600 hover:bg-green-700 transition-all rounded-lg py-2 font-semibold shadow-lg hover:shadow-green-500/30"
          >
            Salva modifiche
          </button>
        </form>

        <button
          onClick={() => router.push("/home")}
          className="mt-4 text-sm text-gray-300 hover:text-white transition underline-offset-2 hover:underline w-full text-center"
        >
          ← Torna alla Home
        </button>
      </div>
    </div>
  );
}
