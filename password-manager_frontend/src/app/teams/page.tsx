"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { useVault } from "@/Components/AuthGate/VaultContext";
import { getTeamsByUserId } from "@/api/apis";
import { team } from "@/api/entities/team";
import "./teams.css";

export default function TeamsPage() {
  const vault = useVault();
  const [teams, setTeams] = useState<team[] | null>(null);

  useEffect(() => {
    getTeamsByUserId(vault.user.id).then(setTeams);
  }, [vault.user.id]);

  const sorted = teams
    ? [...teams].sort((a, b) => Number(b.is_personal) - Number(a.is_personal))
    : null;

  return (
    <div className="teams-page">
      <div className="teams-header">
        <h1>Teams</h1>
        <Link href="/teams/new" className="teams-new-btn">+ New team</Link>
      </div>

      {sorted === null && <p>Loading...</p>}
      {sorted && sorted.length === 0 && <p>No teams yet.</p>}

      <div className="teams-list">
        {sorted?.map((t) => (
          <Link key={t.id} href={`/teams/${t.id}`} className="team-card">
            <span>{t.name}</span>
            {t.is_personal && <span className="badge">Personal</span>}
          </Link>
        ))}
      </div>
    </div>
  );
}
