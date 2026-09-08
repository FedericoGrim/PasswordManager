import Link from "next/link";

// Without a root not-found boundary, Next's client router falls back to a
// full page reload on any unmatched route — which wipes the in-memory vault
// (AuthGate/VaultContext are never persisted). This keeps 404s client-side.
export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">Page not found</h1>
      <Link href="/teams" className="text-blue-600 underline">Back to your teams</Link>
    </div>
  );
}
