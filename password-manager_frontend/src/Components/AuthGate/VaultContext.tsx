"use client";

import { createContext, useContext } from "react";
import { mainUser } from "@/api/entities/mainUser";

// Session-only: never persisted to localStorage/sessionStorage. Populated
// once, at signup or at vault-unlock, and held for the life of the tab.
export type VaultKeys = {
  user: mainUser;
  privateKeyEc: Uint8Array;
  privateKeyPq: Uint8Array;
  masterKey: CryptoKey;
};

export const VaultContext = createContext<VaultKeys | null>(null);

export function useVault(): VaultKeys {
  const vault = useContext(VaultContext);
  if (!vault) throw new Error("useVault() called outside VaultContext.Provider");
  return vault;
}
