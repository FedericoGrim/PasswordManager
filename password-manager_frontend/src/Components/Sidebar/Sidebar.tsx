"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link"; // Usiamo Link per evitare il refresh della pagina
import { Star, Trash2, Users, Settings, ChevronRight } from "lucide-react";
import "./Sidebar.css";

export default function Sidebar() {
  const [settingsMenuOpen, setSettingsMenuOpen] = useState(false);

  return (
    <header className="sidebar">
      {/* GRUPPO SUPERIORE: Logo e Navigazione principale */}
      <div className="sidebar-top-group">
        <Link href="/home" className="logo-link">
          <div className="logo-container">
            <Image
              src="/KeydenLogoWhite.png"
              alt="Logo"
              width={96}
              height={144}
              className="logo-img"
            />
          </div>
        </Link>

        <Link href="/home" className="icon-button">
          <Star className="icon" />
        </Link>

        {/* Trash: no backend concept exists yet (no field, no endpoint) —
            disabled rather than linking to a dead route. */}
        <button className="icon-button" disabled title="Coming soon">
          <Trash2 className="icon" />
        </button>

        <Link href="/teams" className="icon-button">
          <Users className="icon" />
        </Link>
      </div>

      {/* GRUPPO INFERIORE: Impostazioni */}
      <div className="sidebar-bottom-group">
        <div className="relative">
          <div className="menu-button-container">
            <button
              onClick={() => setSettingsMenuOpen((v) => !v)}
              className="menu-button group"
            >
              <Settings className="icon" />
              <div className="menu-arrow group-hover">
                <ChevronRight className="icon arrow-icon" />
              </div>
            </button>
          </div>

          {settingsMenuOpen && (
            <div className="dropdown-menu">
              <Link href="/settings/profile" className="dropdown-link">Profile</Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}