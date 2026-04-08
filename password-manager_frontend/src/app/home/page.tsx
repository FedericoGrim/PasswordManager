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
    <main className="main-layout">
      <section className="content-area">
        {/* 2. COLONNA SINISTRA: Titolo + Preferiti */}
        <div className="column-fav">
          <h1 className={`fav-title ${poppins.className}`}>KEYDEN</h1>
          <FavMenu />
        </div>

        {/* 3. DIVISORE CENTRALE */}
        <div className="divider"></div>

        {/* 4. COLONNA DESTRA: Menu Ricerca + Griglia */}
        <div className="column-menu">
          <Menu />
        </div>
      </section>
    </main>
  );
}
