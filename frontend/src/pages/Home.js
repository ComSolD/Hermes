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
                          {match.home_pts}:{match.away_pts}
                        </td>
                        <td>
                          {tournament.name === "NFL"
                        ? `${match.stage}`
                        : `${match.date}`} {match.time}
                        </td>
                      </tr>

                    </tbody>
                  </table>
                  <table>
                  <thead>
                      <tr>
                        <th>Победитель</th>
                        <th>Линия</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr key={match.match_id}>
                        <td>
                          {match.match_bet.ml_result}
                        </td>
                        <td>
                          {match.match_bet.ml_odds}
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
