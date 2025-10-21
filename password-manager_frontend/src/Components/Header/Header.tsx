"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Avatar from "@mui/material/Avatar";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { deepOrange } from "@mui/material/colors";
import Image from "next/image";
import Link from "next/link";

import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export default function Header() {
  const [AnchorEl, SetAnchorEl] = useState<null | HTMLElement>(null);
  const [Username, SetUsername] = useState("U"); // fallback
  const router = useRouter();
  const IsMenuOpen = Boolean(AnchorEl);

  useEffect(() => {
    // Leggi sessionStorage solo lato client
    const storedUsername = sessionStorage.getItem("Username");
    if (storedUsername) SetUsername(storedUsername);
  }, []);

  const FirstLetter = Username.charAt(0).toUpperCase();

  function HandleClick(event: React.MouseEvent<HTMLElement>) {
    SetAnchorEl(event.currentTarget);
  }

  function HandleClose() {
    SetAnchorEl(null);
  }

  function Logout() {
    sessionStorage.clear();
    const RealmUrl = "http://localhost:8080/realms/PasswordManager";
    const ClientId = "PasswordManager-frontend";
    const RedirectUrl = "http://localhost:3000/login-register";
    const LogoutUrl = `${RealmUrl}/protocol/openid-connect/logout?client_id=${ClientId}&post_logout_redirect_uri=${encodeURIComponent(RedirectUrl)}`;
    window.location.href = LogoutUrl;
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#070e15]/90 backdrop-blur border-b border-gray-800 shadow-md">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3">
        {/* Logo e titolo */}
        <div className="flex items-center gap-2">
          <Link href="/home">
            <Image
              src="/PasswordManagerIcon.png"
              alt="Keyden logo"
              width={36}
              height={36}
              className="cursor-pointer"
            />
          </Link>
          <Link
            href="/home"
            className="text-xl font-semibold text-white hover:text-[#35C6EE] transition"
          >
            Keyden
          </Link>
        </div>

        {/* Avatar e menu */}
        <div>
          <Avatar
            sx={{ bgcolor: "#070e15", cursor: "pointer" }}
            onClick={HandleClick}
            id="avatar-button"
          >
            <AccountCircleIcon fontSize="large" />
          </Avatar>

          <Menu
            anchorEl={AnchorEl}
            open={IsMenuOpen}
            onClose={HandleClose}
            MenuListProps={{ "aria-labelledby": "avatar-button" }}
            PaperProps={{
              sx: {
                backgroundColor: "#1e1e22",
                color: "#fff",
                border: "1px solid #333",
                boxShadow: "0 4px 10px rgba(0,0,0,0.5)",
              },
            }}
          >
            <MenuItem
              onClick={() => {
                HandleClose();
                router.push("/profile");
              }}
              sx={{ "&:hover": { backgroundColor: "#2a2a2f" } }}
            >
              Profilo
            </MenuItem>
            <MenuItem
              onClick={() => {
                HandleClose();
                Logout();
              }}
              sx={{ "&:hover": { backgroundColor: "#2a2a2f" } }}
            >
              Logout
            </MenuItem>
          </Menu>
        </div>
      </div>
    </header>
  );
}
