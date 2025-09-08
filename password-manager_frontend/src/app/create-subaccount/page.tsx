"use client";

import { useState, useEffect } from "react";
import { createSubAccount } from "../../api/apis";
import { useRouter } from "next/navigation";
import { subAccount } from "@/api/entities/subAccount";
import { v4 as uuidv4 } from "uuid";
import { UUID } from "crypto";
import { Encrypt } from "../crypto/decript";

export default function CreateSubAccountPage() {
  const [UserId, SetUserId] = useState<UUID | null>(null);
  const [KeyBuffer, SetKeyBuffer] = useState<Buffer | null>(null);

  const [form, setForm] = useState<Partial<subAccount>>({
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
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
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-6">Crea nuovo subaccount</h1>
      <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
        <label>
          Titolo:
          <input
            type="text"
            name="title"
            value={form.title}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
            required
          />
        </label>
        <label>
          Username:
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
            required
          />
        </label>
        <label>
          URL:
          <input
            type="text"
            name="url"
            value={form.url}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
          />
        </label>
        <label>
          Password:
          <input
            type="text"
            name="password"
            value={form.password}
            onChange={handleChange}
            className="border rounded px-2 py-1 w-full"
            required
          />
        </label>
        <button
          type="submit"
          className="px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700"
        >
          Crea subaccount
        </button>
      </form>
    </div>
  );
}
