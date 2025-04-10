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
        <MenuItem 
          title="NBA" 
          links={["Расписание", "Гибкая статистика", "Таблица"]} 
          paths={["/nba/schedule", "/nba/statistic", "/nba/standings"]} 
        />
        <MenuItem 
          title="MLB" 
          links={["Расписание", "Гибкая статистика", "Таблица"]} 
          paths={["/mlb/schedule", "/mlb/statistic", "/mlb/standings"]} 
        />
        <MenuItem 
          title="NHL" 
          links={["Расписание", "Гибкая статистика", "Таблица"]} 
          paths={["/nhl/schedule", "/nhl/statistic", "/nhl/standings"]} 
        />
      </nav>
    </header>
  );
};


const MenuItem = ({ title, links, paths }) => {
  return (
    <div className="dropdown">
      <Link to="#" className="menu-title">{title}</Link>
      <div className="dropdown-menu">
        {links.map((link, index) => (
          <Link key={index} to={paths[index]}>
            {link}
          </Link>
        ))}
      </div>
    </div>
  );
};


export default Header;
