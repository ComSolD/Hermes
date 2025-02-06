import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "./components/Header";
import "./MatchDetail.css";

function MatchDetailNBA() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nba/match/${id}`) // Загружаем данные о матче
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
        <div className="match-title">
          <h1>{match.match_info.home_team} vs {match.match_info.away_team}</h1>
          <p>Дата: {match.match_info.date}</p>
          <p>Стадия: {match.stage}</p>
        </div>

        {/* Нижние два блока */}
        <div className="team-info-container">
          {/* Блок 1 - Инфа о первой команде */}
          <div className="team-info">
            <h2>{match.match_info.home_team}</h2>
            <p>Игроки: </p>
            <p>Тренер: </p>
          </div>

          {/* Блок 2 - Инфа о второй команде */}
          <div className="team-info">
            <h2>{match.match_info.away_team}</h2>
            <p>Игроки: </p>
            <p>Тренер: </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default MatchDetailNBA;
