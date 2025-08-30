"use client";

import { useEffect, useState } from "react";
import { 
  getMainUserByKeycloakId, 
  getSubAccountsByUserId,
  deleteSubAccount
} from "../api/apis";

import { mainUser } from "@/api/entities/mainUser";
import { subAccount } from "@/api/entities/subAccount";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const [user, setUser] = useState<mainUser | null>(null);
  const [subAccounts, setSubAccounts] = useState<subAccount[]>([]);
  const router = useRouter();

  useEffect(() => {
    getMainUserByKeycloakId("3fa85f64-5717-4562-b3fc-2c963f66afa6").then(setUser);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (user?.Id) {
        const data = await getSubAccountsByUserId(user.Id);
        setSubAccounts(data);
      }
    };
    fetchData();
  }, [user]);

  const HandleDeleteSubAccount = async (sa: subAccount) => {
      if (!confirm("Sei sicuro di voler eliminare questo subaccount?")) return;
      await deleteSubAccount( sa.id);
      setSubAccounts(prev => prev.filter(s => s.id !== sa.id));
  };

  if (!user) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-6">
        Benvenuto, il tuo ID è: {user.Id}
      </h1>

      <button 
        onClick={() => {
          sessionStorage.setItem("userId", JSON.stringify(user.Id));
          sessionStorage.setItem("userSalt", user.SaltArgon ?? "");
          sessionStorage.setItem("masterPassword", JSON.stringify("string"));
          router.push("/create-subaccount");
        }}
        className="mb-6 px-4 py-2 bg-green-600 text-white rounded-lg shadow hover:bg-green-700"
      >
        ➕ Crea nuovo subaccount
      </button>

      <h2 className="text-lg font-semibold mb-4">I tuoi sottoconti:</h2>
      {subAccounts.length === 0 ? (
        <div className="text-gray-600 italic mb-4">
          Nessun subaccount registrato a questo account
        </div>
      ) : (
        <ul className="space-y-4">
          {subAccounts.map((sa) => (
            <li 
              key={sa.id} 
              className="p-4 rounded-2xl shadow-md border border-[#005F73] bg-[#0A9396] flex flex-col gap-2 text-[#001219]"
            >
              <p><strong>Title:</strong> {sa.title}</p>
              <p><strong>Username:</strong> {sa.username}</p>
              <p>
                <strong>URL:</strong> 
                <a href={sa.url} target="_blank" rel="noopener noreferrer" className="underline text-blue-700 ml-2">
                  {sa.url}
                </a>
              </p>
              <p><strong>ID:</strong> {sa.id}</p>

              <div className="flex gap-4 mt-2">
                <button 
                  onClick={() => {
                    sessionStorage.setItem("subAccountData", JSON.stringify(sa));
                    sessionStorage.setItem("userSalt", user.SaltArgon ?? "");
                    router.push("/edit-subaccount");
                  }}
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
