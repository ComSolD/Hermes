import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNBA";
import "../../styles/MatchDetail.css";

function MoneylineDetailNBA() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nba/match/${id}/moneyline`) // Загружаем данные о матче
      .then((response) => response.json())
      .then((data) => {
        setMatch(data)
        document.title = `${data.match_info.home_team} vs ${data.match_info.away_team}`;
      })
      .catch((error) => console.error("Ошибка загрузки:", error));


  }, [id]);

  if (!match) {
    return (
      <div>
        <Header />
        <h1 style={{textAlign: "center"}}>Загрузка...</h1>
      </div>
    );
  }

  return (

    <div>
      <Header />
      <main className="match-main">
        {/* Верхний блок с инфой о матче */}
        <MatchHeader match={match} id={id} />

        <div className="block-info">
          <table className="bet-info">
            <thead>
              <tr>
                <th>Период</th>
                <th>
                  <div className="team-name-cell">
                    <img src={match.match_info.home_team_logo || '/default_logo.png'} alt="logo" className="team-logo" />
                    <span>{match.match_info.home_team}</span>
                  </div>
                </th>
                <th>
                  <div className="team-name-cell">
                    <img src={match.match_info.away_team_logo || '/default_logo.png'} alt="logo" className="team-logo" />
                    <span>{match.match_info.away_team}</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
            {match.match_info.moneyline_info.map((ml, index) => {
                // Определяем, какие данные использовать для текущего периода
                let homeScore, awayScore;

                switch (ml.period) {
                  case "1-я Четверть":
                    homeScore = match.match_info.total.home_q1;
                    awayScore = match.match_info.total.away_q1;
                    break;
                  case "2-я Четверть":
                    homeScore = match.match_info.total.home_q2;
                    awayScore = match.match_info.total.away_q2;
                    break;
                  case "3-я Четверть":
                    homeScore = match.match_info.total.home_q3;
                    awayScore = match.match_info.total.away_q3;
                    break;
                  case "4-я Четверть":
                    homeScore = match.match_info.total.home_q4;
                    awayScore = match.match_info.total.away_q4;
                    break;
                  case "1-я Половина":
                    homeScore =
                      match.match_info.total.home_q1 + match.match_info.total.home_q2;
                    awayScore =
                      match.match_info.total.away_q1 + match.match_info.total.away_q2;
                    break;
                  case "2-я Половина":
                    homeScore =
                      match.match_info.total.home_q3 + match.match_info.total.home_q4;
                    awayScore =
                      match.match_info.total.away_q3 + match.match_info.total.away_q4;
                    break;
                  default:
                    homeScore = match.match_info.total.home_total;
                    awayScore = match.match_info.total.away_total;
                }

                // Определяем стиль
                const homeStyle =
                  homeScore > awayScore
                    ? { fontWeight: "bold", color: "#4CAF50"}
                    : awayScore === homeScore
                    ? { fontWeight: "bold", color: "#FFC107"}
                    : { fontWeight: "bold", color: "#FF0000"};
                const awayStyle =
                  awayScore > homeScore
                    ? { fontWeight: "bold", color: "#4CAF50"}
                    : awayScore === homeScore
                    ? { fontWeight: "bold", color: "#FFC107"}
                    : { fontWeight: "bold", color: "#FF0000"};

                return (
                  <tr key={index}>
                    <td>{ml.period}</td>
                    <td style={homeStyle}>{ml.home_odds}</td>
                    <td style={awayStyle}>{ml.away_odds}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

      </main>
    </div>
  );
}

export default MoneylineDetailNBA;
