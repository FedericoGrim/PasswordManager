"use client";

import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { deepOrange } from "@mui/material/colors";
import { UUID } from "crypto";

export default function AvatarMenu() {
  const [AnchorEl, SetAnchorEl] = React.useState<null | HTMLElement>(null);
  const Open = Boolean(AnchorEl);
  const [UserId, SetUserId] = React.useState<UUID | null>(null);

  const HandleClick = (event: React.MouseEvent<HTMLElement>) => {
    SetAnchorEl(event.currentTarget);
  };

  const HandleClose = () => {
    SetAnchorEl(null);
  };

  React.useEffect(() => {
    const Id = sessionStorage.getItem("UserId") as UUID | null;
    SetUserId(Id);
  }, []);

  return (
    <>
      {/* Topbar con altezza fissa */}
      <div className="h-20 w-full bg-gray-200 flex items-center px-4">
        <h1 className="text-lg font-bold">Dashboard</h1>
      </div>

      {/* Avatar fisso in alto a destra */}
      <div className="fixed top-4 right-4 z-50">
        <Avatar
          sx={{ bgcolor: deepOrange[500], cursor: "pointer" }}
          onClick={HandleClick}
        >
          {UserId ? UserId.toString()[0] : "?"}
        </Avatar>

        <Menu
          anchorEl={AnchorEl}
          open={Open}
          onClose={HandleClose}
          slotProps={{
            list: { "aria-labelledby": "avatar-button" },
          }}
        >
          <MenuItem onClick={HandleClose}>Profile</MenuItem>
          <MenuItem onClick={HandleClose}>My account</MenuItem>
          <MenuItem onClick={HandleClose}>Logout</MenuItem>
        </Menu>
      </div>
    </>
  );
}
