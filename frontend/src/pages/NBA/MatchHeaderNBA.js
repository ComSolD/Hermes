import React from "react";
import { Link } from "react-router-dom";

const MatchHeader = ({ match, id }) => {
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
              <th>4</th>
              <th>T</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{match.match_info.home_team}</td>
              <td>{match.match_info.total.home_q1}</td>
              <td>{match.match_info.total.home_q2}</td>
              <td>{match.match_info.total.home_q3}</td>
              <td>{match.match_info.total.home_q4}</td>
              <td>{match.match_info.total.home_total}</td>
              <td>Стадия: {match.stage}</td>
            </tr>
          </tbody>
          <tbody>
            <tr>
              <td>{match.match_info.away_team}</td>
              <td>{match.match_info.total.away_q1}</td>
              <td>{match.match_info.total.away_q2}</td>
              <td>{match.match_info.total.away_q3}</td>
              <td>{match.match_info.total.away_q4}</td>
              <td>{match.match_info.total.away_total}</td>
              <td>Дата: {match.match_info.date}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Навигационные вкладки */}
      <div className="block-info">
        <div className="tab-content">
          <Link to={`/nba/match/${id}`} className="tab">
            Статистика
          </Link>
          <Link to={`/nba/match/${id}/total`} className="tab">
            Тотал
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MatchHeader;
