"use client";

import { useState, useEffect } from "react";
import { createSubAccount } from "../../api/apis";
import { useRouter } from "next/navigation";
import { subAccount } from "@/api/entities/subAccount";
import { v4 as uuidv4 } from "uuid";
import { UUID } from "crypto";
import { Encrypt } from "../../Functions/Cripting-Decripting/Cript-Dectipr";

import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import CasinoIcon from "@mui/icons-material/Casino"

export default function CreateSubAccountPage() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [passwordLength, setPasswordLength] = useState(12);

  const [form, SetForm] = useState<Partial<subAccount>>({
    title: "",
    username: "",
    url: "",
    password: ""
  });

  const router = useRouter();

  useEffect(() => {
    const storedUserId = sessionStorage.getItem("UserId") as UUID | null;
    const KeyRaw = sessionStorage.getItem("Key");

    SetUserId(storedUserId);

    if (KeyRaw) {
      const Buf = Buffer.from(
        KeyRaw.match(/.{1,2}/g)!.map(b => parseInt(b, 16))
      );
      SetKeyBuffer(Buf);
    }
  }, []);

  const HandleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    SetForm({ ...form, [e.target.name]: e.target.value });
  };

  const HandleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!UserId) {
      alert("UserId mancante!");
      return;
    }
    if (!KeyBuffer) {
      alert("Chiave di cifratura mancante!");
      return;
    }

    const newSubAccount: subAccount = {
      ...form,
      id: uuidv4(),
      user_id: UserId,
      password: Encrypt(form.password ?? "", KeyBuffer),
      url: form.url ?? "",
      title: form.title ?? "",
      username: form.username ?? ""
    } as subAccount;

    try {
      await createSubAccount(UserId, newSubAccount);
      alert("Subaccount creato!");
      router.push("/home");
    } catch (err) {
      alert("Errore nella creazione del subaccount");
      console.error(err);
    }
  };

  const GenerateRandomPassword = (length: number) => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#@!";
    let password = "";
    for (let i = 0; i < length; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    SetForm({ ...form, password });
  };

  return (
    <div className="min-h-screen bg-[#0D1B2A] flex items-center justify-center p-6">
      <div className="bg-[#1B263B]/90 backdrop-blur-lg rounded-2xl shadow-2xl p-8 w-full max-w-md text-white border border-white/20">
        <h1 className="text-2xl font-bold mb-6 text-center">Crea nuovo subaccount</h1>

        <form className="flex flex-col gap-5" onSubmit={HandleSubmit}>
          {["title", "username", "url"].map(field => (
            <div key={field}>
              <label className="block text-sm font-medium mb-1 capitalize">{field}</label>
              <input
                type="text"
                name={field}
                value={form[field as keyof typeof form] || ""}
                onChange={HandleChange}
                className="w-full rounded-lg px-3 py-2 bg-[#0D1B2A] border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                placeholder={`Inserisci ${field}`}
                required
              />
            </div>
          ))}

          {/* Password con mostra/nascondi e genera casuale */}
          <div className="flex flex-col">
            <label className="block text-sm font-medium mb-1 capitalize">Password</label>
            <div className="flex items-center gap-2">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={form.password || ""}
                onChange={HandleChange}
                className="flex-1 rounded-lg px-3 py-2 bg-[#0D1B2A] border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                placeholder="••••••••"
                required
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
                className="w-16 text-wjite rounded-lg px-2 py-1 border border-gray-500"
                title="Lunghezza password"
              />
              <button
                type="button"
                onClick={() => GenerateRandomPassword(passwordLength)}
                className="p-2 bg-[#243447] rounded-lg hover:bg-[#2c3e50] transition text-white text-sm font-semibold border border-gray-500"
              >
                <CasinoIcon></CasinoIcon>
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="mt-2 bg-green-600 hover:bg-green-700 transition-all rounded-lg py-2 font-semibold shadow-lg hover:shadow-green-500/30"
          >
            Crea Subaccount
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
