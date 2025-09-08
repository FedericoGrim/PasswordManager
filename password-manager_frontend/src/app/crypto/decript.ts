import { Buffer } from "buffer";
import crypto from "crypto";

export function Encrypt(data: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);

  let encrypted = cipher.update(data, "utf8");
  encrypted = Buffer.concat([encrypted, cipher.final()]);

  const payload = Buffer.concat([iv, encrypted]);
  return payload.toString("base64"); 
}

export function Decrypt(encryptedData: string, key: Buffer): string {
  if (!encryptedData) throw new Error("Encrypted data is undefined");

  const raw = Buffer.from(encryptedData, "base64");
  const iv = raw.subarray(0, 16);
  const ciphertext = raw.subarray(16);

  const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);

  return decrypted.toString("utf8"); // ⚡ Node gestisce il padding
}



export function DeriveKey(masterPassword: string, salt: Buffer): Buffer {
  return crypto.pbkdf2Sync(masterPassword, salt, 100000, 32, "sha256");
}

export function GenerateSalt(): Buffer {
  return crypto.randomBytes(16);
}
