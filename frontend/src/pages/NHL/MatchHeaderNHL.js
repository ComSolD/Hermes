import React from "react";
import { Link, useLocation } from "react-router-dom";

const MatchHeader = ({ match, id }) => {
  const location = useLocation();
  
  return (
    <div className="match-header">
      {/* Заголовок матча */}
      <div className="match-title">
        <h1>{match.match_info.home_team} vs {match.match_info.away_team}</h1>
        <table>
          <thead>
            <tr>
              <th></th>
              <th>1</th>
              <th>2</th>
              <th>3</th>
              <th>T{match.match_info.match_status !== "Maintime" ? ` ${match.match_info.match_status}` : ""}</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{match.match_info.home_team}</td>
              <td>{match.match_info.total.home_p1}</td>
              <td>{match.match_info.total.home_p2}</td>
              <td>{match.match_info.total.home_p3}</td>
              <td>{match.match_info.total.home_total}</td>
              <td>Стадия: {match.stage}</td>
            </tr>
          </tbody>
          <tbody>
            <tr>
              <td>{match.match_info.away_team}</td>
              <td>{match.match_info.total.away_p1}</td>
              <td>{match.match_info.total.away_p2}</td>
              <td>{match.match_info.total.away_p3}</td>
              <td>{match.match_info.total.away_total}</td>
              <td>Дата: {match.match_info.date}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Навигационные вкладки */}
      <div className="block-info">
        <div className="tab-content">
          <Link 
            to={location.pathname === `/nhl/match/${id}` ? "#" : `/nhl/match/${id}`} 
            className={`tab ${location.pathname === `/nhl/match/${id}` ? "active" : ""}`}
            onClick={(e) => location.pathname === `/nhl/match/${id}` && e.preventDefault()}
          >
            Статистика
          </Link>

          <Link 
            to={location.pathname.includes("/1x2") ? "#" : `/nhl/match/${id}/1x2`} 
            className={`tab ${location.pathname.includes("/1x2") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/1x2") && e.preventDefault()}
          >
            1x2
          </Link>

          <Link 
            to={location.pathname.includes("/moneyline") ? "#" : `/nhl/match/${id}/moneyline`} 
            className={`tab ${location.pathname.includes("/moneyline") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/moneyline") && e.preventDefault()}
          >
            Исход
          </Link>

          <Link 
            to={location.pathname.includes("/total") ? "#" : `/nhl/match/${id}/total/0`} 
            className={`tab ${location.pathname.includes("/total") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/total") && e.preventDefault()}
          >
            Тотал
          </Link>

          <Link 
            to={location.pathname.includes("/handicap") ? "#" : `/nhl/match/${id}/handicap/0`} 
            className={`tab ${location.pathname.includes("/handicap") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/handicap") && e.preventDefault()}
          >
            Фора
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MatchHeader;
