import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNHL";
import "../../styles/MatchDetail.css";

function XBetDetailNHL() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nhl/match/${id}/1x2`) // Загружаем данные о матче
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
                <th>{match.match_info.home_team}</th>
                <th>X</th>
                <th>{match.match_info.away_team}</th>
              </tr>
            </thead>
            <tbody>
            {match.match_info.xbet_info.map((ml, index) => {
                // Определяем, какие данные использовать для текущего периода
                let homeScore, awayScore;

                switch (ml.period) {
                  case "1-й Период":
                    homeScore = match.match_info.total.home_p1;
                    awayScore = match.match_info.total.away_p1;
                    break;
                  case "2-й Период":
                    homeScore = match.match_info.total.home_p2;
                    awayScore = match.match_info.total.away_p2;
                    break;
                  case "3-й Период":
                    homeScore = match.match_info.total.home_p3;
                    awayScore = match.match_info.total.away_p3;
                    break;
                  default:
                    homeScore = match.match_info.total.home_total;
                    awayScore = match.match_info.total.away_total;
                }

                // Определяем стиль
                const homeStyle =
                  homeScore > awayScore
                    ? { fontWeight: "bold", color: "#4CAF50"}
                    : { fontWeight: "bold", color: "#FF0000"};
                const awayStyle =
                  awayScore > homeScore
                    ? { fontWeight: "bold", color: "#4CAF50"}
                    : { fontWeight: "bold", color: "#FF0000"};
                const drawStyle =
                  awayScore === homeScore
                    ? { fontWeight: "bold", color: "#4CAF50"}
                    : { fontWeight: "bold", color: "#FF0000"};

                return (
                  <tr key={index}>
                    <td>{ml.period}</td>
                    <td style={homeStyle}>{ml.home_odds}</td>
                    <td style={drawStyle}>{ml.draw}</td>
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

export default XBetDetailNHL;
