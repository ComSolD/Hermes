import React, { useEffect, useState  } from "react";

import Header from "../../components/Header";
import "../../styles/Statistic.css";


function StatisticNBA() {
  const [seasons, setSeasons] = useState([]); // Храним сезоны
  const [stages, setStages] = useState([]); // Храним стадии
  const [teams, setTeams] = useState([]); // Храним команды

  const [selectedSeason, setSelectedSeason] = useState("");
  const [selectedStage, setSelectedStage] = useState("");
  const [selectedTeam, setSelectedTeam] = useState("");

  const [answer, setAnswer] = useState("");


  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nba/statistic`) // Загружаем данные о матче
      .then((response) => response.json())
      .then((data) => {
        document.title = `Статистика`;

        setSeasons(data.seasons || []);
        setStages(data.stages || []);
        setTeams(data.teams || []);
      })
      .catch((error) => console.error("Ошибка загрузки:", error));


  }, []);

  const handleSubmit = () => {
    const requestData = {
      season: selectedSeason,
      stage: selectedStage,
      team_id: selectedTeam
    };

    fetch("http://127.0.0.1:8000/api/nba/filterstat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestData)
    })
      .then((response) => response.json())
      .then((data) => {
        setAnswer(data.answer || []);
      })
      .catch((error) => console.error("Ошибка при отправке:", error));
  };

  return (
    <div>
      <Header />
      <main className="statistic-main">
        <div className="statistic-info">
          <div className="selectors">
              {/* Сезон */}
            <div className="selector">
              <label htmlFor="season-select">Сезон</label>
              <select
                id="season-select"
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
              >
                <option value="">Все сезоны</option>
                {seasons.map((season, index) => (
                  <option key={index} value={season}>
                    {season}
                  </option>
                ))}
              </select>
            </div>

              {/* Стадия */}
            <div className="selector">
              <label htmlFor="stage-select">Стадия</label>
              <select
                id="stage-select"
                value={selectedStage}
                onChange={(e) => setSelectedStage(e.target.value)}
              >
                <option value="">Все стадии</option>
                {stages.map((stage, index) => (
                  <option key={index} value={stage}>
                    {stage}
                  </option>
                ))}
              </select>
            </div>

            {/* Команда */}
            <div className="selector">
              <label htmlFor="team-select">Команда</label>
              <select
                id="team-select"
                value={selectedTeam}
                onChange={(e) => setSelectedTeam(e.target.value)}
              >
                <option value="">Все команды</option>
                {teams.map((team) => (
                  <option key={team.team_id} value={team.team_id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button className="submit-button" onClick={handleSubmit}>
            Отправить
          </button>
          <div className="results">
            <h3>Результаты</h3>
            {answer}
          </div>
        </div>
      </main>
    </div>
  );
}

export default StatisticNBA;