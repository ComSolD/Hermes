import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNHL";
import "../../styles/MatchDetail.css";
import { Link } from "react-router-dom";

function TotalDetailNHL() {
  const { id, period  } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nhl/match/${id}/total/${period || 0}`) // Загружаем данные о матче
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
                to={`/nhl/match/${id}/total/${p.number}`} // Динамический URL
                className={`tab ${Number(period) === p.number ? "active" : ""}`} // Подсветка активного периода
                onClick={(e) => Number(period) === p.number && e.preventDefault()}
              >
                {p.period}
              </Link>
            ))}
            </div>

            <table className="odds-list">
              <thead>
                <th>Тотал</th>
                <th>Меньше</th>
                <th>Больше</th>
              </thead>
              <tbody>
              {match.match_info.total_odds.map((t, index) => {
                  let firstScore, secondScore;
                  switch (t.period) {
                    case 0:
                      firstScore = match.match_info.match_status !== "Maintime" ? match.match_info.total.away_total - 1 : match.match_info.total.away_total;
                      secondScore = match.match_info.total.home_total;
                      break;
                    case 1:
                      firstScore = match.match_info.total.home_p1;
                      secondScore = match.match_info.total.away_p1;
                      break;
                    case 2:
                      firstScore = match.match_info.total.home_p2;
                      secondScore = match.match_info.total.away_p2;
                      break;
                    case 3:
                      firstScore = match.match_info.total.home_p3;
                      secondScore = match.match_info.total.away_p3;
                      break;
                    default:
                      firstScore = match.match_info.total.away_total;
                      secondScore = match.match_info.total.home_total;
                  }

                  // Определяем стиль
                  const underStyle =
                    firstScore + secondScore < t.total
                      ? { fontWeight: "bold", color: "#4CAF50"}
                      : firstScore + secondScore === t.total
                      ? { fontWeight: "bold", color: "#FFC107"}
                      : { fontWeight: "bold", color: "#FF0000"};
                  const overStyle =
                    firstScore + secondScore > t.total
                      ? { fontWeight: "bold", color: "#4CAF50"}
                      : firstScore + secondScore === t.total
                      ? { fontWeight: "bold", color: "#FFC107"}
                      : { fontWeight: "bold", color: "#FF0000"};
                  
                  return (<tr key={index}>
                    <td>{t.total}</td>
                    <td style={underStyle}>{t.under_odds}</td>
                    <td style={overStyle}>{t.over_odds}</td>
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
