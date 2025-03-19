import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNHL";
import "../../styles/MatchDetail.css";
import { Link } from "react-router-dom";


function TotalDetailNHL() {
  const { id, period } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nhl/match/${id}/handicap/${period || 0}`) // Загружаем данные о матче
      .then((response) => response.json())
      .then((data) => {
        setMatch(data)
        document.title = `${data.match_info.home_team} vs ${data.match_info.away_team}`;
      })
      .catch((error) => console.error("Ошибка загрузки:", error));


  }, [id, period]);

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
          <div className="tab-content">
            {match.match_info.periods.map((p) => (
              <Link
                key={p.number}
                to={`/nhl/match/${id}/handicap/${p.number}`} // Динамический URL
                className={`tab ${Number(period) === p.number ? "active" : ""}`} // Подсветка активного периода
                onClick={(e) => Number(period) === p.number && e.preventDefault()}
              >
                {p.period}
              </Link>
            ))}
          </div>
          <table className="odds-list">
            <thead>
              <th>Фора</th>
              <th>{match.match_info.home_team}</th>
              <th>{match.match_info.away_team}</th>
            </thead>
            <tbody>
              {match.match_info.handicap_odds.map((h, index) => {
                  

                  // Определяем стиль
                  const homeStyle =
                    "win" === h.handicap_team2_result
                      ? { fontWeight: "bold", color: "#4CAF50"}
                      : "lose" === h.handicap_team2_result
                      ? { fontWeight: "bold", color: "#FF0000"}
                      : "draw" === h.handicap_team2_result
                      ? { fontWeight: "bold", color: "#FFC107"}
                      : {};
                  const awayStyle =
                    "win" === h.handicap_team1_result
                      ? { fontWeight: "bold", color: "#4CAF50"}
                      : "lose" === h.handicap_team1_result
                      ? { fontWeight: "bold", color: "#FF0000"}
                      : "draw" === h.handicap_team1_result
                      ? { fontWeight: "bold", color: "#FFC107"}
                      : {};
                  
                  return (<tr key={index}>
                    <td>{h.handicap > 0 ? "+" : ''}{h.handicap}{h.handicap !== 0 ? (h.handicap > 0 ? "-" : "+") : ""}</td>
                    <td style={homeStyle}>{h.handicap_team2_odds}</td>
                    <td style={awayStyle}>{h.handicap_team1_odds}</td>
                  </tr>)
              })}
              </tbody>
          </table>
          
        </div>

      </main>
    </div>
  );
}

export default TotalDetailNHL;
