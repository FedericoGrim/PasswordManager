import argon2 from "argon2-browser";

const enc = new TextEncoder();
const dec = new TextDecoder();

export async function deriveMasterKey(
  masterPassword: string,
  salt: Uint8Array,
  parametri: { m: number; t: number; p: number }
): Promise<CryptoKey> {
  const { hash } = await argon2.hash({
    pass: masterPassword,
    salt,
    type: argon2.ArgonType.Argon2id,
    mem: parametri.m,
    time: parametri.t,
    parallelism: parametri.p,
    hashLen: 32,
  });
  return crypto.subtle.importKey("raw", hash, "AES-GCM", false, ["encrypt", "decrypt"]);
}

export async function encrypt(dato: string, chiave: CryptoKey): Promise<string> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const cifrato = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, chiave, enc.encode(dato));
  const payload = new Uint8Array(iv.length + cifrato.byteLength);
  payload.set(iv);
  payload.set(new Uint8Array(cifrato), iv.length);
  return btoa(String.fromCharCode(...payload));
}

export async function decrypt(payloadB64: string, chiave: CryptoKey): Promise<string> {
  const payload = Uint8Array.from(atob(payloadB64), (c) => c.charCodeAt(0));
  const iv = payload.subarray(0, 12);
  const cifrato = payload.subarray(12);
  const chiaro = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, chiave, cifrato);
  return dec.decode(chiaro);
}

export function generateSalt(): Uint8Array {
  return crypto.getRandomValues(new Uint8Array(16));
}