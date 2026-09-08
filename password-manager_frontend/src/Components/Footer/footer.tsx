export default function Footer() {
  return (
    <footer className="text-[#4465ad] text-sm py-4 text-center">
      © {new Date().getFullYear()}{" "}
      <span className="text-[#271d66] font-semibold">Keyden</span> — Proteggi le tue credenziali con sicurezza
    </footer>
  );
}
