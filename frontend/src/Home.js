import React, { useEffect, useState } from "react";
import "./Home.css";
import Header from "./components/Header";
import { Link } from "react-router-dom";

function Home() {
  const [tournaments, setTournaments] = useState([]);

  useEffect(() => {
    document.title = "Главная страница";

    // Загрузка данных с сервера
    fetch("http://127.0.0.1:8000/api/") // Укажите ваш URL
      .then((response) => response.json())
      .then((data) => setTournaments(data))
      .catch((error) => console.error("Ошибка загрузки:", error));
  }, []);

  return (
    <div>
      <Header />
      <main className="main-content">
        {tournaments.map((tournament, index) => (
          <div className="league-block" key={index}>
            <div className="league-title">{tournament.name}</div>
            <h2 className="future-match">Будущие матчи:</h2>
            {tournament.upcoming_matches.length > 0 ? (
              tournament.upcoming_matches.map((match) => (
                <div key={match.match_id} className="match">
                  <Link to={`/match/${match.match_id}`}>
                    <h3>{match.home_team} vs {match.away_team}</h3>
                  </Link>

                  <table>
                    <thead>
                        <tr>
                          <th>Победа</th>
                          <th>Тотал {match.total}</th>
                          <th>Фора</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr key={match.match_id}>
                          <td>
                            {match.home_team}
                            <div style={{ textAlign: "center"}}>
                              {match.ml_home}
                            </div>
                          </td>
                          <td>
                            Больше
                            <div style={{ textAlign: "center"}}>
                              {match.total_over}
                            </div>
                          </td>
                          <td>
                            {match.spread_home > 0 ? `+${match.spread_home}` : match.spread_home}
                            <div style={{ textAlign: "center"}}>
                              {match.spread_home_parlay}
                            </div>
                          </td>
                        </tr>
                        <tr key={match.match_id}>
                          <td>
                            {match.away_team}
                            <div style={{ textAlign: "center"}}>
                              {match.ml_away}
                            </div>
                          </td>
                          <td>
                            Меньше
                            <div style={{ textAlign: "center"}}>
                              {match.total_under}
                            </div>
                          </td>
                          <td>
                            {match.spread_away > 0 ? `+${match.spread_away}` : match.spread_away}
                            <div style={{ textAlign: "center"}}>
                              {match.spread_away_parlay}
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                  <p style={{ textAlign: "right"}}>{tournament.name === "NFL"
                      ? `Стадия: ${match.stage}`
                      : `Дата: ${match.date}`}
                  </p>
                </div>
              ))
            ) : (
              <p>Нет данных о будущих матчах</p>
            )}

            <h2 className="past-match">Прошедшие матчи:</h2>
            {tournament.past_matches.length > 0 ? (
              tournament.past_matches.map((match) => (
                <div key={match.match_id} className="match">
                  <Link to={`/match/${match.match_id}`}>
                    <h3>{match.home_team} vs {match.away_team}</h3>
                  </Link>
                  <table>
                    <tbody>
                      <tr key={match.match_id}>
                        <td>
                          {match.ml_result}
                        </td>
                        <td>
                          {match.away_pts}:{match.home_pts}
                        </td>
                        <td>
                          {tournament.name === "NFL"
                        ? `${match.stage}`
                        : `${match.date}`}
                        </td>
                      </tr>

                    </tbody>
                  </table>
                  <table>
                  <thead>
                      <tr>
                        <th>Победа</th>
                        <th>Тотал</th>
                        <th>Фора</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr key={match.match_id}>
                        <td>
                          {match.ml_result}
                          <div style={{ textAlign: "center"}}>
                            {match.ml_parlay}
                          </div>
                        </td>
                        <td>
                          {match.total_result === "over" ? "Больше" : "Меньше"} {match.total}
                          <div style={{ textAlign: "center"}}>
                            {match.total_parlay}
                          </div>
                        </td>
                        <td>
                          {match.spread_result}
                          <div style={{ textAlign: "center"}}>
                          {match.spread_parlay} {match.spread > 0 ? `+${match.spread}` : match.spread}
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              ))
            ) : (
              <p>Нет данных о прошедших матчах</p>
            )}

            <div className="update-time">Обновлено: {tournament.updated_at} МСК</div>
          </div>
        ))}
      </main>
    </div>
  );
}

export default Home;
