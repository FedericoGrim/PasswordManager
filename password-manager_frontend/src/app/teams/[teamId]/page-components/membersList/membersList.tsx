"use client";

import { useEffect, useState } from "react";

import { getTeamMembersByTeamId, getUserById } from "@/api/apis";
import { teamPermLevel } from "@/api/entities/teamPermLevel";
import "./membersList.css";

type ResolvedMember = { memberId: string; username: string; code: string; permLevelName: string };

export default function MembersList({ teamId, permLevels }: { teamId: string; permLevels: teamPermLevel[] }) {
  const [members, setMembers] = useState<ResolvedMember[] | null>(null);

  useEffect(() => {
    let cancelled = false;

    getTeamMembersByTeamId(teamId).then(async (rows) => {
      const resolved = await Promise.all(
        rows.map(async (m) => {
          const user = await getUserById(m.user_id);
          const permLevel = permLevels.find((pl) => pl.id === m.perm_level_id);
          return {
            memberId: m.id,
            username: user?.username ?? "(unknown)",
            code: user?.code ?? "",
            permLevelName: permLevel?.name ?? "",
          };
        })
      );
      if (!cancelled) setMembers(resolved);
    });

    return () => {
      cancelled = true;
    };
  }, [teamId, permLevels]);

  if (members === null) return <p>Loading members...</p>;

  return (
    <ul className="members-list">
      {members.map((m) => (
        <li key={m.memberId} className="members-list-item">
          <span className="members-list-name">{m.username}#{m.code}</span>
          <span className="members-list-role">{m.permLevelName}</span>
        </li>
      ))}
    </ul>
  );
}
