import { useEffect } from "react";

export const useFetchFilters = ({ filters, activeFilters, setTeams, setPlayers, setOpponents, setSeasons, setStages }) => {
  useEffect(() => {
    if (activeFilters.includes("team_id")) {
      fetch("http://127.0.0.1:8000/api/nba/teams_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setTeams(data.teams || []))
        .catch((err) => console.error("Ошибка загрузки команд:", err));
    }
  }, [filters, activeFilters, setTeams]);

  useEffect(() => {
    if (activeFilters.includes("player_id")) {
      fetch("http://127.0.0.1:8000/api/nba/players_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setPlayers(data.players || []))
        .catch((err) => console.error("Ошибка загрузки игроков:", err));
    }
  }, [filters, activeFilters, setPlayers]);

  useEffect(() => {
    if (activeFilters.includes("opponent_id")) {
      fetch("http://127.0.0.1:8000/api/nba/opponents_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setOpponents(data.opponents || []))
        .catch((err) => console.error("Ошибка загрузки оппонентов:", err));
    }
  }, [filters, activeFilters, setOpponents]);

  useEffect(() => {
    if (activeFilters.includes("season")) {
      fetch("http://127.0.0.1:8000/api/nba/seasons_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setSeasons(data.seasons || []))
        .catch((err) => console.error("Ошибка загрузки сезонов:", err));
    }
  }, [filters, activeFilters, setSeasons]);

  useEffect(() => {
    if (activeFilters.includes("stage")) {
      fetch("http://127.0.0.1:8000/api/nba/stages_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setStages(data.stages || []))
        .catch((err) => console.error("Ошибка загрузки стадий:", err));
    }
  }, [filters, activeFilters, setStages]);
};
