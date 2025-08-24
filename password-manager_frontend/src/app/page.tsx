"use client";

import { useEffect, useState } from "react";
import { getMainUserByKeycloakId } from "../api/apis";

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    getMainUserByKeycloakId("3fa85f64-5717-4562-b3fc-2c963f66afa6").then(setUser);
  }, []);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>Benvenuto {user.Name}</h1>
    </div>
  );
}
