// The bundled build inlines its WASM as base64 so it has no wasm/fs imports
// for Turbopack/webpack to resolve — see Cript-Dectipr.ts for why we use it
// over the package's default entry. No .d.ts ships with this subpath, so
// reuse @types/argon2-browser's shape for it.
declare module "argon2-browser/dist/argon2-bundled.min.js" {
  import argon2 from "argon2-browser";
  export default argon2;
}
