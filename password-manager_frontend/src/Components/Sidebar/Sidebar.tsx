"use client";

import { useState } from "react";
import { Home, Star, Trash2, Users, Settings, ChevronRight } from "lucide-react";
import "./Sidebar.css";

export default function Sidebar() {
  const [usersMenuOpen, setUsersMenuOpen] = useState(false);
  const [settingsMenuOpen, setSettingsMenuOpen] = useState(false);

  return (
    <header className="sidebar">
      {/* Logo */}
      <a href="/home" className="logo-link">
        <div className="logo-container">
          <div className="logo-inner">
            <img src="/KeydenLogo.png" alt="Keyden Logo" className="logo-img" />
          </div>
        </div>
      </a>

      {/* Star */}
      <a href="/favorites" className="icon-button">
        <Star className="icon" />
      </a>

      {/* Trash */}
      <a href="/trash" className="icon-button">
        <Trash2 className="icon" />
      </a>

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
            <a href="/users" className="dropdown-link">Users</a>
            <a href="/teams" className="dropdown-link">Teams</a>
          </div>
        )}
      </div>

      {/* Settings menu */}
      <div className="relative mt-auto mb-4">
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
            <a href="/settings/profile" className="dropdown-link">Profile</a>
            <a href="/settings/security" className="dropdown-link">Security</a>
          </div>
        )}
      </div>
    </header>
  );
}
