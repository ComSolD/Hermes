import React, { useEffect, useState } from "react";
import Select from "react-select";
import Header from "../../components/Header";
import "../../styles/MatchDetail.css";

import { customMainSelectorStyles } from "../../styles/customSelectStyles";


function StandingsNHL() {
  const [seasons, setSeasons] = useState([]);
  const [league, setLeague] = useState(null);
  const [standings, setStandings] = useState([]);

  const [selectedSeason, setSelectedSeason] = useState(null);

  const leagueOptions = [
    { value: null, label: "Все лиги" },
    { value: "Eastern Conference", label: "Восточная Конференция" },
    { value: "Western Conference", label: "Западная Конференция" },
  ];

  useEffect(() => {
    fetch('http://localhost:8000/api/nhl/seasons/')
      .then((res) => res.json())
      .then((data) => {
        const allSeasons = data.seasons || [];
        setSeasons(allSeasons);
        if (allSeasons.length > 0) {
          setSelectedSeason(allSeasons[0]);
        }
      })
      .catch((err) => console.error('Ошибка загрузки сезонов:', err));
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();
    if (selectedSeason) params.append("season", selectedSeason);
    if (league) params.append("league", league);

    fetch(`http://127.0.0.1:8000/api/nhl/standings/?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setStandings(data.results || []))
      .catch((err) => console.error("Ошибка загрузки таблицы:", err));
  }, [seasons, league, selectedSeason]);

  return (
    <div>
      <Header />
      <main className="match-main">
        <div className="block-info">
          <h1>Турнирная таблица NHL</h1>

          <div style={{ display: 'flex', gap: '1rem', marginBottom: '10px' }}>
            <Select
              options={seasons.map(season => ({ value: season, label: season }))}
              styles={customMainSelectorStyles}
              value={selectedSeason ? { value: selectedSeason, label: selectedSeason } : null}
              onChange={(option) => setSelectedSeason(option.value)}
            />

            <Select
              options={leagueOptions}
              styles={customMainSelectorStyles}
              value={leagueOptions.find((opt) => opt.value === league)}
              onChange={(opt) => setLeague(opt.value)}
            />
          </div>

          <div>
            <table>
              <thead>
                <tr>
                  <th>Команда</th>
                  <th>W</th>
                  <th>L</th>
                  <th>Дома</th>
                  <th>Выезд</th>
                  <th>Очки</th>
                  <th>Пропущено</th>
                </tr>
              </thead>
              <tbody>
                {standings.map((team) => (
                  <tr key={team.team_id} className="border-t">
                    <td>
                      <div className="team-name-table">
                        <img src={team.logo || '/default_logo.png'} alt="logo" className="team-logo" />
                        {team.name}
                      </div>
                    </td>
                    <td>{team.wins}</td>
                    <td>{team.losses}</td>
                    <td>{team.home_record}</td>
                    <td>{team.away_record}</td>
                    <td>{team.avg_score}</td>
                    <td>{team.avg_conceded}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </main>
      
    </div>
  );
}

export default StandingsNHL;

