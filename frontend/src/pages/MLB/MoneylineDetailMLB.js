import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderMLB";
import "../../styles/MatchDetail.css";

function MoneylineDetailMLB() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/mlb/match/${id}/moneyline`) // Загружаем данные о матче
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
                <th>{match.match_info.away_team}</th>
              </tr>
            </thead>
            <tbody>
            {match.match_info.moneyline_info.map((ml, index) => {
                // Определяем, какие данные использовать для текущего периода
                let homeScore, awayScore;

                switch (ml.period) {
                  case "1-й Иннинг":
                    homeScore = match.match_info.total.home_i1;
                    awayScore = match.match_info.total.away_i1;
                    break;
                  case "2-й Иннинг":
                    homeScore = match.match_info.total.home_i2;
                    awayScore = match.match_info.total.away_i2;
                    break;
                  case "3-й Иннинг":
                    homeScore = match.match_info.total.home_i3;
                    awayScore = match.match_info.total.away_i3;
                    break;
                  case "4-й Иннинг":
                    homeScore = match.match_info.total.home_i4;
                    awayScore = match.match_info.total.away_i4;
                    break;
                  case "5-й Иннинг":
                    homeScore = match.match_info.total.home_i5;
                    awayScore = match.match_info.total.away_i5;
                    break;
                  case "6-й Иннинг":
                    homeScore = match.match_info.total.home_i6;
                    awayScore = match.match_info.total.away_i6;
                    break;
                  case "7-й Иннинг":
                    homeScore = match.match_info.total.home_i7;
                    awayScore = match.match_info.total.away_i7;
                    break;
                  case "8-й Иннинг":
                    homeScore = match.match_info.total.home_i8;
                    awayScore = match.match_info.total.away_i8;
                    break;
                  case "9-й Иннинг":
                    homeScore = match.match_info.total.home_i9;
                    awayScore = match.match_info.total.away_i9;
                    break;
                  case "1-я Половина":
                    homeScore =
                      match.match_info.total.home_i1 + match.match_info.total.home_i2 + match.match_info.total.home_i3 + match.match_info.total.home_i4 + match.match_info.total.home_i5;
                    awayScore =
                      match.match_info.total.away_i1 + match.match_info.total.away_i2 + match.match_info.total.away_i3 + match.match_info.total.away_i4 + match.match_info.total.away_i5;
                    break;
                  case "2-я Половина":
                    homeScore =
                      match.match_info.total.home_i6 + match.match_info.total.home_i7 + match.match_info.total.home_i8 + match.match_info.total.home_i9;
                    awayScore =
                      match.match_info.total.away_i6 + match.match_info.total.away_i7 + match.match_info.total.away_i8 + match.match_info.total.away_i9;
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

export default MoneylineDetailMLB;
