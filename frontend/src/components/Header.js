import React, { useState } from "react";
import "./Header.css";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="header">
      {/* Логотип */}
      <div className="logo">
        <img
          src="/image.png"
          alt="React Logo"
          style={{ width: "40px", marginRight: "10px" }}
        />
        InsightFlow
      </div>

      {/* Кнопка гамбургер-меню */}
      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
        ☰
      </button>

      {/* Навигация */}
      <nav className={menuOpen ? "nav open" : "nav"}>
        <a href="#nba">NBA</a>
        <a href="#nfl">NFL</a>
        <a href="#nhl">NHL</a>
        <a href="#mlb">MLB</a>
      </nav>
    </header>
  );
};

export default Header;
