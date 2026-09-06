import { generateSymmetricTeamKey, wrapTeamKey, base64ToBytes } from "../Cripting-Decripting/Cript-Dectipr";
import { getTeamMembersByTeamId, getUserById, updateUserTeamsKey } from "../../api/apis";

// Rotates a team's symmetric key: generates a fresh key client-side, then
// re-wraps it for every current member with that member's own EC+PQ public
// keys (each member decrypts the same new key with a different wrap). The
// plaintext key never leaves the browser.
export async function rotateTeamKey(teamId: string, interactorId: string): Promise<Uint8Array> {
  const newTeamKeyRaw = generateSymmetricTeamKey();
  const members = await getTeamMembersByTeamId(teamId);

  for (const member of members) {
    const recipient = await getUserById(member.user_id);
    if (!recipient) continue;

    const wrapped = await wrapTeamKey(
      newTeamKeyRaw,
      base64ToBytes(recipient.public_key_ec),
      base64ToBytes(recipient.public_key_pq)
    );

    await updateUserTeamsKey(
      { user_id: member.user_id, team_id: teamId, team_key_encrypted: wrapped },
      interactorId
    );
  }

  return newTeamKeyRaw;
}
