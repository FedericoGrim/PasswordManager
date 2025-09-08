"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { DeriveKey } from "../crypto/decript";
import { getMainUserByKeycloakId } from "@/api/apis";
import { mainUser } from "@/api/entities/mainUser";
import { UUID } from "crypto";

const LoginPage = () => {
  const Router = useRouter();
  const [Email, setEmail] = useState("");
  const [Password, setPassword] = useState("");

  const HandleLogin = async () => {
    const user: mainUser | null = await getMainUserByKeycloakId("3fa85f64-5717-4562-b3fc-2c963f66afa6");
    if (!user) {
      console.error("User not found");
      return;
    }
    const key = await DeriveKey(Password, user.SaltArgon ? Buffer.from(user.SaltArgon, "hex") : Buffer.from(""));
    console.log("UserId:", user.Id, "Key:", key, "Salt:", user.SaltArgon);
    sessionStorage.setItem("UserId", user.Id as UUID);
    sessionStorage.setItem("Key", key.toString("hex"));
    sessionStorage.setItem("Salt", user.SaltArgon);
    Router.push("/home");
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
      <div style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px" }}>
        <h1>Login</h1>
        <input
          type="email"
          placeholder="Email"
          value={Email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: "10px", fontSize: "16px" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={Password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ padding: "10px", fontSize: "16px" }}
        />
        <button
          onClick={HandleLogin}
          style={{ padding: "10px", fontSize: "16px", cursor: "pointer" }}
        >
          Accedi
        </button>
      </div>
    </div>
  );
};

export default LoginPage;
