"use client";

import FavMenu from "./page-components/favMenu/favMenu";
import Menu from "./page-components/menu/menu";

import "./styles.css";

export default function Home() {
  return (
    <section className="flex flex-1 gap-0">
      {/* Colonna sinistra */}
      <div className="flex-1 flex flex-col overflow-auto">
        <h1 className="fav-title">Keyden</h1>
        <FavMenu />
      </div>

      {/* Divider */}
      <div className="divider"></div>

      {/* Colonna destra */}
      <div className="flex-1 overflow-auto">
        <Menu />
      </div>
    </section>
  );
}