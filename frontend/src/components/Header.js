import React, { useState } from "react";
import "./Header.css";
import { Link } from "react-router-dom";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="header">
      {/* Логотип */}
      <div className="logo">
        
      <Link to="/" style={{ display: "flex", alignItems: "center", textDecoration: "none", color: "inherit" }}>
        <img
          src="/image.png"
          alt="React Logo"
          style={{ width: "40px", marginRight: "10px" }}
        />
        InsightFlow
      </Link>
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
