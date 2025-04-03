import { useEffect } from "react";

export const useFetchFilters = ({ filters, activeFilters, setTeams, setPlayers, setOpponents, setSeasons, setStages, setHomeAway }) => {
  useEffect(() => {
    if (activeFilters.includes("team_id")) {
      fetch("http://127.0.0.1:8000/api/mlb/teams_by_filters/", {
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
      fetch("http://127.0.0.1:8000/api/mlb/players_by_filters/", {
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
      fetch("http://127.0.0.1:8000/api/mlb/opponents_by_filters/", {
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
      fetch("http://127.0.0.1:8000/api/mlb/seasons_by_filters/", {
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
    if (activeFilters.includes("homeaway")) {
      fetch("http://127.0.0.1:8000/api/mlb/homeaway_by_filters/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setHomeAway(data.homeaways || []))
        .catch((err) => console.error("Ошибка загрузки положения:", err));
    }
  }, [filters, activeFilters, setHomeAway]);

  useEffect(() => {
    if (activeFilters.includes("stage")) {
      fetch("http://127.0.0.1:8000/api/mlb/stages_by_filters/", {
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
