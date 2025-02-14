import React, { useEffect, useState } from "react";
import "../styles/Home.css";
import Header from "../components/Header";
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
                  <Link to={`/${tournament.name.toLowerCase()}/match/${match.match_id}`}>
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
                              {match.match_bet.ml_home}
                            </div>
                          </td>
                          <td>
                            Больше
                            <div style={{ textAlign: "center"}}>
                              {match.match_bet.total_over}
                            </div>
                          </td>
                          <td>
                            {match.match_bet.handicap_home > 0 ? `+${match.match_bet.handicap_home}` : match.match_bet.handicap_home}
                            <div style={{ textAlign: "center"}}>
                              {match.match_bet.handicap_home_parlay}
                            </div>
                          </td>
                        </tr>
                        <tr key={match.match_id}>
                          <td>
                            {match.away_team}
                            <div style={{ textAlign: "center"}}>
                              {match.match_bet.ml_away}
                            </div>
                          </td>
                          <td>
                            Меньше
                            <div style={{ textAlign: "center"}}>
                              {match.match_bet.total_under}
                            </div>
                          </td>
                          <td>
                            {match.match_bet.handicap_away > 0 ? `+${match.match_bet.handicap_away}` : match.match_bet.handicap_away}
                            <div style={{ textAlign: "center"}}>
                              {match.match_bet.handicap_away_parlay}
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
                  <Link to={`/${tournament.name.toLowerCase()}/match/${match.match_id}`}>
                    <h3>{match.home_team} vs {match.away_team}</h3>
                  </Link>
                  <table>
                    <tbody>
                      <tr key={match.match_id}>
                        <td>
                          {match.match_bet.ml_result}
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
                          {match.match_bet.ml_result}
                          <div style={{ textAlign: "center"}}>
                            {match.match_bet.ml_parlay}
                          </div>
                        </td>
                        <td>
                          {match.match_bet.total_result === "over" ? "Больше" : "Меньше"} {match.match_bet.total}
                          <div style={{ textAlign: "center"}}>
                            {match.match_bet.total_parlay}
                          </div>
                        </td>
                        <td>
                          {match.match_bet.handicap_result}
                          <div style={{ textAlign: "center"}}>
                          {match.match_bet.handicap_parlay} {match.match_bet.handicap > 0 ? `+${match.match_bet.handicap}` : match.match_bet.handicap}
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
