import React from "react";
import Select from "react-select";

export const TeamSelector = ({ teams, filters, updateFilter, customSelectorStyles }) => {
  const options = teams.map((team) => ({ value: team.team_id, label: team.name }));
  const currentValue = options.find((opt) => opt.value === filters.team_id) || null;

  return (
    <Select
      options={[{ value: "", label: "Все команды" }, ...options]}
      value={currentValue}
      onChange={(selectedOption) => updateFilter("team_id", selectedOption?.value || "")}
      placeholder="Выберите команду..."
      styles={customSelectorStyles}
      isSearchable
      isDisabled={options.length === 0}
    />
  );
};

export const PlayerSelector = ({ players, filters, updateFilter, customSelectorStyles }) => {
  const options = players.map((player) => ({ value: player.player_id, label: player.name }));
  const currentValue = options.find((opt) => opt.value === filters.player_id) || null;

  return (
    <Select
      options={[{ value: "", label: "Все игроки" }, ...options]}
      value={currentValue}
      onChange={(selectedOption) => updateFilter("player_id", selectedOption?.value || "")}
      placeholder="Выберите игрока..."
      styles={customSelectorStyles}
      isSearchable
      isDisabled={options.length === 0}
    />
  );
};

export const OpponentSelector = ({ opponents, filters, updateFilter, customSelectorStyles }) => {
  const options = opponents.map((opponent) => ({ value: opponent.team_id, label: opponent.name }));
  const currentValue = options.find((opt) => opt.value === filters.opponent_id) || null;

  return (
    <Select
      options={[{ value: "", label: "Все оппоненты" }, ...options]}
      value={currentValue}
      onChange={(selectedOption) => updateFilter("opponent_id", selectedOption?.value || "")}
      placeholder="Выберите оппонента..."
      styles={customSelectorStyles}
      isSearchable
      isDisabled={options.length === 0}
    />
  );
};

export const StageSelector = ({ stages, filters, updateFilter, customSelectorStyles }) => {
  const options = stages.map((stage) => ({ value: stage.value, label: stage.label }));
  const currentValue = options.find((opt) => opt.value === filters.stage) || null;

  return (
    <Select
      options={[{ value: "", label: "Все стадии" }, ...options]}
      value={currentValue}
      onChange={(selected) => updateFilter("stage", selected?.value || "")}
      placeholder="Выберите стадию..."
      isSearchable
      isDisabled={options.length === 0}
      styles={customSelectorStyles}
      classNamePrefix="custom-select"
    />
  );
};

export const SeasonSelector = ({ seasons, filters, updateFilter, customSelectorStyles }) => {
  const options = seasons.map((season) => ({ value: season, label: season }));
  const currentValue = options.find((opt) => opt.value === filters.season) || null;

  return (
    <Select
      options={[{ value: "", label: "Все сезоны" }, ...options]}
      value={currentValue}
      onChange={(selected) => updateFilter("season", selected?.value || "")}
      placeholder="Выберите сезон..."
      isSearchable
      isDisabled={options.length === 0}
      styles={customSelectorStyles}
      classNamePrefix="custom-select"
    />
  );
};
