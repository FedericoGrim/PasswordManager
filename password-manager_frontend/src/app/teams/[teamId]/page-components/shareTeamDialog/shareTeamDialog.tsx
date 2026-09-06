"use client";

import { FormEvent, useState } from "react";

import { getUserByUsernameAndCode, createTeamPermLevel, addMemberToTeam, addUserTeamsKey } from "@/api/apis";
import { wrapTeamKey, base64ToBytes } from "@/Functions/Cripting-Decripting/Cript-Dectipr";
import { teamPermLevel } from "@/api/entities/teamPermLevel";
import "./shareTeamDialog.css";

const DEFAULT_SHARE_PERM_LEVEL_NAME = "Member";
const DEFAULT_SHARE_PERM_LEVEL_RANK = 1;

export default function ShareTeamDialog({
  teamId,
  teamKeyRaw,
  interactorId,
  permLevels,
  onClose,
  onShared,
}: {
  teamId: string;
  teamKeyRaw: Uint8Array;
  interactorId: string;
  permLevels: teamPermLevel[];
  onClose: () => void;
  onShared: () => void;
}) {
  const [username, setUsername] = useState("");
  const [code, setCode] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const target = await getUserByUsernameAndCode(username, code);
      if (!target) {
        setError("No user found with that username and code.");
        return;
      }

      let shareLevel = permLevels.find((pl) => pl.name === DEFAULT_SHARE_PERM_LEVEL_NAME);
      if (!shareLevel) {
        shareLevel = await createTeamPermLevel(
          { team_id: teamId, name: DEFAULT_SHARE_PERM_LEVEL_NAME, rank: DEFAULT_SHARE_PERM_LEVEL_RANK },
          interactorId
        );
      }

      const wrappedForTarget = await wrapTeamKey(
        teamKeyRaw,
        base64ToBytes(target.public_key_ec),
        base64ToBytes(target.public_key_pq)
      );

      await addMemberToTeam({ user_id: target.id, team_id: teamId, perm_level_id: shareLevel.id }, interactorId);
      await addUserTeamsKey({ user_id: target.id, team_id: teamId, team_key_encrypted: wrappedForTarget }, interactorId);

      onShared();
    } catch (err) {
      console.error("Error sharing team:", err);
      setError("Could not share this team. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="share-dialog-overlay" onClick={onClose}>
      <form onSubmit={handleSubmit} onClick={(e) => e.stopPropagation()} className="share-dialog">
        <h2>Share this team</h2>
        <p>Enter the other user&apos;s username and code (shown on their profile page).</p>

        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} required />

        <label>Code</label>
        <input value={code} onChange={(e) => setCode(e.target.value)} required maxLength={10} />

        {error && <p className="share-dialog-error">{error}</p>}

        <div className="share-dialog-actions">
          <button type="button" onClick={onClose} disabled={submitting}>Cancel</button>
          <button type="submit" disabled={submitting}>{submitting ? "Sharing..." : "Share"}</button>
        </div>
      </form>
    </div>
  );
}
