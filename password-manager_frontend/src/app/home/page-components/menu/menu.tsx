"use client";

import { useMemo, useState } from "react";
import "./menu.css";

const ITEMS_PER_PAGE = 6;

type GridItem = {
  id: number;
  title: string;
};

const items: GridItem[] = Array.from({ length: 40 }, (_, i) => ({
  id: i + 1,
  title: `Title ${i + 1}`,
}));

export default function Menu() {
  const [searchText, setSearchText] = useState("");
  const [currentPage, setCurrentPage] = useState(1);

  // 🔹 filtro dati
  const filteredItems = useMemo(() => {
    return items.filter((item) =>
      item.title.toLowerCase().includes(searchText.toLowerCase())
    );
  }, [searchText]);

  // 🔹 paginazione
  const totalPages = Math.ceil(filteredItems.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const visibleItems = filteredItems.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );

  // 🔹 pagine visibili (max 3)
  const getPagesToShow = () => {
    if (totalPages <= 3) return Array.from({ length: totalPages }, (_, i) => i + 1);
    if (currentPage === 1) return [1, 2, 3];
    if (currentPage === totalPages) return [totalPages - 2, totalPages - 1, totalPages];
    return [currentPage - 1, currentPage, currentPage + 1];
  };

  const pagesToShow = getPagesToShow();

  return (
    <div className="grid-container">
      {/* SEARCH */}
      <div className="grid-search">
        <input
          type="text"
          placeholder="SEARCH..."
          value={searchText}
          onChange={(e) => {
            setSearchText(e.target.value);
            setCurrentPage(1);
          }}
        />
        <button className="filter-btn">⏷</button>
      </div>

      {/* GRID */}
      <div className="grid">
        {visibleItems.map((item) => (
          <button
            key={item.id}
            className="grid-card"
            onClick={() => console.log(item)}
          >
            {item.title}
          </button>
        ))}
      </div>

      {/* PAGINATION */}
      <div className="grid-pagination">
        <button
          className="pagination-arrow"
          onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          disabled={currentPage === 1}
        >
          ‹
        </button>

        {pagesToShow.map((page) => (
          <button
            key={page}
            className={`pagination-page ${page === currentPage ? "active" : ""}`}
            onClick={() => setCurrentPage(page)}
          >
            {page}
          </button>
        ))}

        <button
          className="pagination-arrow"
          onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
        >
          ›
        </button>
      </div>
    </div>
  );
}
