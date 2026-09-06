import { v4 as uuidv4 } from "uuid";

import {
  generateSalt,
  generateEcKeyPair,
  generatePqKeyPair,
  generateSymmetricTeamKey,
  wrapTeamKey,
  deriveMasterKey,
  encrypt,
  bytesToBase64,
  ARGON2_PARAMS,
} from "../Cripting-Decripting/Cript-Dectipr";
import { createMainUser } from "../../api/apis";
import { mainUser } from "../../api/entities/mainUser";

const USER_CODE_LENGTH = 10;
const USER_CODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

function generateUserCode(length = USER_CODE_LENGTH): string {
  const bytes = crypto.getRandomValues(new Uint8Array(length));
  return Array.from(bytes, (b) => USER_CODE_ALPHABET[b % USER_CODE_ALPHABET.length]).join("");
}

// Runs once, on a Keycloak user's first login: generates this user's EC+PQ
// keypairs and a personal-team key client-side, wraps the private keys with
// a key derived from the master password, wraps the team key for the EC+PQ
// public keys, and registers all of it with the backend in one call. The
// backend never sees the master password or any plaintext private key.
export type ProvisionedVault = {
  user: mainUser;
  privateKeyEc: Uint8Array;
  privateKeyPq: Uint8Array;
  masterKey: CryptoKey;
};

export async function provisionUser(
  keycloakId: string,
  username: string,
  masterPassword: string
): Promise<ProvisionedVault> {
  const salt = generateSalt();

  const ec = await generateEcKeyPair();
  const pq = await generatePqKeyPair();
  const teamKeyRaw = generateSymmetricTeamKey();

  const masterKey = await deriveMasterKey(masterPassword, salt, ARGON2_PARAMS);
  const privateKeyEcEncrypted = await encrypt(bytesToBase64(ec.privateKey), masterKey);
  const privateKeyPqEncrypted = await encrypt(bytesToBase64(pq.privateKey), masterKey);

  const teamKeyEncrypted = await wrapTeamKey(teamKeyRaw, ec.publicKey, pq.publicKey);

  const user = new mainUser({
    id: uuidv4(),
    keycloak_id: keycloakId,
    username,
    code: generateUserCode(),
    salt: bytesToBase64(salt),
    public_key_ec: bytesToBase64(ec.publicKey),
    private_key_ec: privateKeyEcEncrypted,
    public_key_pq: bytesToBase64(pq.publicKey),
    private_key_pq: privateKeyPqEncrypted,
    team_key_encrypted: teamKeyEncrypted,
  });

  const created = await createMainUser(user);
  return {
    user: created,
    privateKeyEc: ec.privateKey,
    privateKeyPq: pq.privateKey,
    masterKey,
  };
}
