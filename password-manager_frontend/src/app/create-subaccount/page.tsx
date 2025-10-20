"use client";

import { useState, useEffect } from "react";
import { createSubAccount } from "../../api/apis";
import { useRouter } from "next/navigation";
import { subAccount } from "@/api/entities/subAccount";
import { v4 as uuidv4 } from "uuid";
import { UUID } from "crypto";
import { Encrypt } from "../../Functions/Cripting-Decripting/Cript-Dectipr";

export default function CreateSubAccountPage() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);

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

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-6">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 w-full max-w-md text-white border border-white/20">
        <h1 className="text-2xl font-bold mb-6 text-center">
          Crea nuovo subaccount
        </h1>

        <form className="flex flex-col gap-5" onSubmit={HandleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1">Titolo</label>
            <input
              type="text"
              name="title"
              value={form.title}
              onChange={HandleChange}
              className="w-full rounded-lg px-3 py-2 bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={HandleChange}
              className="w-full rounded-lg px-3 py-2 bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">URL</label>
            <input
              type="text"
              name="url"
              value={form.url}
              onChange={HandleChange}
              className="w-full rounded-lg px-3 py-2 bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="text"
              name="password"
              value={form.password}
              onChange={HandleChange}
              className="w-full rounded-lg px-3 py-2 bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
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
