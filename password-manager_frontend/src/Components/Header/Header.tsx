"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Avatar from "@mui/material/Avatar";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { deepOrange } from "@mui/material/colors";
import Image from "next/image";
import Link from "next/link";

export default function Header() {
  const [AnchorEl, SetAnchorEl] = useState<null | HTMLElement>(null);
  const IsMenuOpen = Boolean(AnchorEl);
  const router = useRouter();

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

    const LogoutUrl = `${RealmUrl}/protocol/openid-connect/logout?client_id=${ClientId}&post_logout_redirect_uri=${encodeURIComponent(
      RedirectUrl
    )}`;
    window.location.href = LogoutUrl;
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur border-b border-gray-200 shadow-sm ">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3 ">
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
            className="text-xl font-semibold text-[#2563eb] hover:opacity-80 transition"
          >
            Keyden
          </Link>
        </div>

        {/* Avatar e menu */}
        <div>
          <Avatar
            sx={{ bgcolor: deepOrange[500], cursor: "pointer" }}
            onClick={HandleClick}
            id="avatar-button"
          >
            K
          </Avatar>

          <Menu
            anchorEl={AnchorEl}
            open={IsMenuOpen}
            onClose={HandleClose}
            MenuListProps={{ "aria-labelledby": "avatar-button" }}
          >
            <MenuItem
              onClick={() => {
                HandleClose();
                router.push("/profile");
              }}
            >
              Profilo
            </MenuItem>
            <MenuItem
              onClick={() => {
                HandleClose();
                Logout();
              }}
            >
              Logout
            </MenuItem>
          </Menu>
        </div>
      </div>
    </header>
  );
}
