"use client";

import { useEffect, useState } from "react";
import { getMainUserByKeycloakId, getSubAccountsByUserId } from "../api/apis";

import { mainUser } from "@/api/entities/mainUser";
import { subAccount } from "@/api/entities/subAccount";

export default function ProfilePage() {
  const [user, setUser] = useState<mainUser | null>(null);
  const [subAccount, setSubAccount] = useState<subAccount[]>([]);

  useEffect(() => {
    getMainUserByKeycloakId("3fa85f64-5717-4562-b3fc-2c963f66afa9").then(setUser);
    getSubAccountsByUserId("6ff9e31e-0b64-4c7d-a972-37893f98841c").then(setSubAccount);
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>Benvenuto, il tuo ID è: {user.Id}</h1>

      <h2>I tuoi sottoconti:</h2>
      <ul>
        {subAccount.map((sa, index) => (
          <li key={index}>
            {JSON.stringify(sa)}
          </li>
        ))}
      </ul>
    </div>
  );
}
