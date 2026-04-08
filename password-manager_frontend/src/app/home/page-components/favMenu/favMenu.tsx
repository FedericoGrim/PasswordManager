"use client";

import { useState } from "react";
import "./favMenu.css";

type FavItem = {
  id: number;
  title: string;
};

const ITEMS_PER_PAGE = 6;

const favItems: FavItem[] = Array.from({ length: 20 }, (_, i) => ({
  id: i + 1,
  title: "Fav Title",
}));

export default function FavMenu() {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(favItems.length / ITEMS_PER_PAGE);

  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const visibleItems = favItems.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE
  );

  const goPrev = () => setCurrentPage((p) => Math.max(1, p - 1));
  const goNext = () => setCurrentPage((p) => Math.min(totalPages, p + 1));

  // max 3 numeri visibili
  const getPagesToShow = () => {
    if (totalPages <= 3) return Array.from({ length: totalPages }, (_, i) => i + 1);

    if (currentPage === 1) return [1, 2, 3];
    if (currentPage === totalPages) return [totalPages - 2, totalPages - 1, totalPages];

    return [currentPage - 1, currentPage, currentPage + 1];
  };

  const pagesToShow = getPagesToShow();

  return (
    <div className="fav-container">
      {/* Griglia: solo bottoni */}
      <div className="fav-grid">
        {visibleItems.map((item) => (
          <button
            key={item.id}
            className="fav-card"
            onClick={() => console.log(item)}
          >
            {item.title}
          </button>
        ))}
      </div>

      {/* Paginazione */}
      <div className="fav-pagination">
        <button className="pagination-arrow" onClick={goPrev} disabled={currentPage === 1}>
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

        <button className="pagination-arrow" onClick={goNext} disabled={currentPage === totalPages}>
          ›
        </button>
      </div>
    </div>
  );
}
