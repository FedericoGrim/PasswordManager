"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link"; // Usiamo Link per evitare il refresh della pagina
import { Star, Trash2, Users, Settings, ChevronRight } from "lucide-react";
import "./Sidebar.css";

export default function Sidebar() {
  const [usersMenuOpen, setUsersMenuOpen] = useState(false);
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

        <Link href="/favorites" className="icon-button">
          <Star className="icon" />
        </Link>

        <Link href="/trash" className="icon-button">
          <Trash2 className="icon" />
        </Link>

        {/* Users menu */}
        <div className="relative">
          <div className="menu-button-container">
            <button
              onClick={() => setUsersMenuOpen((v) => !v)}
              className="menu-button group"
            >
              <Users className="icon" />
              <div className="menu-arrow group-hover">
                <ChevronRight className="icon arrow-icon" />
              </div>
            </button>
          </div>

          {usersMenuOpen && (
            <div className="dropdown-menu">
              <Link href="/users" className="dropdown-link">Users</Link>
              <Link href="/teams" className="dropdown-link">Teams</Link>
            </div>
          )}
        </div>
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
              <Link href="/settings/security" className="dropdown-link">Security</Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}