import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Minimal, self-contained server bundle (.next/standalone) — required to
  // run the app in a distroless Node.js image without full node_modules.
  output: "standalone",
};

export default nextConfig;
