export default function Footer() {
  return (
    <footer className="border-t border-gray-800 text-gray-400 text-sm py-4 text-center bg-[#070e15]/90 backdrop-blur">
      © {new Date().getFullYear()}{" "}
      <span className="text-blue-400 font-semibold">Keyden</span> — Proteggi le tue credenziali con sicurezza
    </footer>
  );
}
