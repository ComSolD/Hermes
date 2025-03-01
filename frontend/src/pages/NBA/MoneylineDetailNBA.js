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
            <h1>Исход</h1>
        </div>

      </main>
    </div>
  );
}

export default MoneylineDetailNBA;
