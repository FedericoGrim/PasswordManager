"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { useVault } from "@/Components/AuthGate/VaultContext";
import { createTeam, createTeamPermLevel, addMemberToTeam, addUserTeamsKey } from "@/api/apis";
import { generateSymmetricTeamKey, wrapTeamKey, base64ToBytes } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import "../teams.css";

const OWNER_PERM_LEVEL_NAME = "Owner";
const OWNER_PERM_LEVEL_RANK = 0;

export default function NewTeamPage() {
  const vault = useVault();
  const router = useRouter();
  const [name, setName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const self = vault.user.id;

      // POST /api/team/ does none of the bootstrapping CreateUserUseCase does
      // for a personal team — replicate it here: Owner perm level, self as
      // member, a fresh team key wrapped for this user's own public keys.
      const newTeam = await createTeam(name, self);
      const owner = await createTeamPermLevel({ team_id: newTeam.id, name: OWNER_PERM_LEVEL_NAME, rank: OWNER_PERM_LEVEL_RANK }, self);
      await addMemberToTeam({ user_id: self, team_id: newTeam.id, perm_level_id: owner.id }, self);

      const teamKeyRaw = generateSymmetricTeamKey();
      const teamKeyEncrypted = await wrapTeamKey(
        teamKeyRaw,
        base64ToBytes(vault.user.public_key_ec),
        base64ToBytes(vault.user.public_key_pq)
      );
      await addUserTeamsKey({ user_id: self, team_id: newTeam.id, team_key_encrypted: teamKeyEncrypted }, self);

      router.push(`/teams/${newTeam.id}`);
    } catch (err) {
      console.error("Error creating team:", err);
      setError("Could not create team. Please try again.");
      setSubmitting(false);
    }
  };

  return (
    <div className="teams-page">
      <h1 className="mb-4">Create a new team</h1>
      <form onSubmit={handleSubmit} className="max-w-sm">
        <label className="block mb-1 text-sm font-medium" htmlFor="name">Team name</label>
        <input
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full mb-4 px-3 py-2 rounded border border-[#415a77]"
        />
        {error && <p className="text-red-700 mb-4">{error}</p>}
        <button
          type="submit"
          disabled={submitting || !name}
          className="teams-new-btn disabled:opacity-50"
        >
          {submitting ? "Creating..." : "Create team"}
        </button>
      </form>
    </div>
  );
}
