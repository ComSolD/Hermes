import React from "react";
import { Link, useLocation } from "react-router-dom";

const MatchHeader = ({ match, id }) => {
  const location = useLocation();
  
  return (
    <div className="match-header">
      {/* Заголовок матча */}
      <div className="match-title">
        <h1>{match.match_info.home_team} vs {match.match_info.away_team}</h1>
        <div>
          <td>Стадия: {match.stage}</td>
          <td>Дата: {match.match_info.date}</td>
        </div>

        <table>
          <thead>
            <tr>
              <th></th>
              <th>1</th>
              <th>2</th>
              <th>3</th>
              <th>4</th>
              <th>5</th>
              <th>6</th>
              <th>7</th>
              <th>8</th>
              <th>9</th>
              <th>H</th>
              <th>R</th>
              <th>E</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{match.match_info.home_team}</td>
              <td>{match.match_info.total.home_i1}</td>
              <td>{match.match_info.total.home_i2}</td>
              <td>{match.match_info.total.home_i3}</td>
              <td>{match.match_info.total.home_i4}</td>
              <td>{match.match_info.total.home_i5}</td>
              <td>{match.match_info.total.home_i6}</td>
              <td>{match.match_info.total.home_i7}</td>
              <td>{match.match_info.total.home_i8}</td>
              <td>{match.match_info.total.home_i9}</td>
              <td>{match.match_info.total.home_hit}</td>
              <td>{match.match_info.total.home_total}</td>
              <td>{match.match_info.total.home_error}</td>
            </tr>
          </tbody>
          <tbody>
            <tr>
              <td>{match.match_info.away_team}</td>
              <td>{match.match_info.total.away_i1}</td>
              <td>{match.match_info.total.away_i2}</td>
              <td>{match.match_info.total.away_i3}</td>
              <td>{match.match_info.total.away_i4}</td>
              <td>{match.match_info.total.away_i5}</td>
              <td>{match.match_info.total.away_i6}</td>
              <td>{match.match_info.total.away_i7}</td>
              <td>{match.match_info.total.away_i8}</td>
              <td>{match.match_info.total.away_i9}</td>
              <td>{match.match_info.total.away_hit}</td>
              <td>{match.match_info.total.away_total}</td>
              <td>{match.match_info.total.away_error}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Навигационные вкладки */}
      <div className="block-info">
        <div className="tab-content">
          <Link 
            to={location.pathname === `/mlb/match/${id}` ? "#" : `/mlb/match/${id}`} 
            className={`tab ${location.pathname === `/mlb/match/${id}` ? "active" : ""}`}
            onClick={(e) => location.pathname === `/mlb/match/${id}` && e.preventDefault()}
          >
            Статистика
          </Link>

          <Link 
            to={location.pathname.includes("/moneyline") ? "#" : `/mlb/match/${id}/moneyline`} 
            className={`tab ${location.pathname.includes("/moneyline") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/moneyline") && e.preventDefault()}
          >
            Исход
          </Link>

          <Link 
            to={location.pathname.includes("/total") ? "#" : `/mlb/match/${id}/total/0`} 
            className={`tab ${location.pathname.includes("/total") ? "active" : ""}`}
            onClick={(e) => location.pathname.includes("/total") && e.preventDefault()}
          >
            Тотал
          </Link>

          <Link 
            to={location.pathname.includes("/handicap") ? "#" : `/mlb/match/${id}/handicap/0`} 
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
