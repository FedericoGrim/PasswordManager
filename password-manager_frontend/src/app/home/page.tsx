"use client";

import FavMenu from "./page-components/favMenu/favMenu";
import Menu from "./page-components/menu/menu";

import { Poppins } from "next/font/google";
import "./styles.css";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export default function Home() {
  return (
    <section className="flex flex-1 gap-0">
      <div className="flex-1 flex flex-col overflow-auto">
        <h1 className={`fav-title ${poppins.className}`}>KEYDEN</h1>
        <FavMenu />
      </div>

      <div className="divider"></div>

      <div className="flex-1 overflow-auto">
        <Menu />
      </div>
    </section>
  );
}
