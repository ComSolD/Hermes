import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "./components/Header";
import "./MatchDetail.css";

function MatchDetail() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nba/match/${id}`) // Загружаем данные о матче
      .then((response) => response.json())
      .then((data) => setMatch(data))
      .catch((error) => console.error("Ошибка загрузки:", error));


  }, [id]);

  useEffect(() => {
    if (match) {
      document.title = `${match.team1} vs ${match.team2}`; // Устанавливаем тайтл
    }
  }, [match]);

  if (!match) {
    return <h1>Загрузка...</h1>;
  }

  return (

    <div>
      <Header />
      <main className="match-main">
        {/* Верхний блок с инфой о матче */}
        <div className="match-title">
          <h1>{match.team1} vs {match.team2}</h1>
          <p>Дата: {match.date}</p>
          <p>Стадия: {match.stage}</p>
        </div>

        {/* Нижние два блока */}
        <div className="team-info-container">
          {/* Блок 1 - Инфа о первой команде */}
          <div className="team-info">
            <h2>{match.team1}</h2>
            <p>Игроки: </p>
            <p>Тренер: {match.coach_team1}</p>
          </div>

          {/* Блок 2 - Инфа о второй команде */}
          <div className="team-info">
            <h2>{match.team2}</h2>
            <p>Игроки: </p>
            <p>Тренер: {match.coach_team2}</p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default MatchDetail;
