import React, { useState } from "react";
import Select from "react-select";

import Header from "../../components/Header";
import "../../styles/Statistic.css";

import { customSelectorStyles, customMainSelectorStyles } from "../../styles/customSelectStyles";

import {
  filterOptions,
  displayOptions,
  statisticOptions,
  limitationOptions
} from "./statistic/statisticOptions";

import { useFetchFilters } from "./statistic/useFetchFilters";

import {
  TeamSelector,
  PlayerSelector,
  OpponentSelector,
  StageSelector,
  SeasonSelector,
  HomeAwaySelector
} from "./statistic/FilterSelectors";

import { createFilterHandlers,
  handleChangeHandicap,
  handleChangeOdds,
  handleChangeTotal,
  blurTotal,
  blurHandicap,
  blurOdds,
 } from "./statistic/filterHandlers";

import {
  getAvailableFilterOptions,
  getAvailableLimitationOptions,
  getAvailableStatisticOptions,
  getAvailableDisplayOptions,
} from "./statistic/optionsLogic";


// Взаимодействует с FilterSelectors.jsx
const filterRenderMap = {
  season: {
    label: "Сезон",
    render: (props) => <SeasonSelector {...props} />,
  },
  stage: {
    label: "Стадия",
    render: (props) => <StageSelector {...props} />,
  },
  homeaway: {
    label: "Положение команды",
    render: (props) => <HomeAwaySelector {...props} />,
  },
  team_id: {
    label: "Команда",
    render: (props) => <TeamSelector {...props} />,
  },
  opponent_id: {
    label: "Оппонент",
    render: (props) => <OpponentSelector {...props} />,
  },
  player_id: {
    label: "Игрок",
    render: (props) => <PlayerSelector {...props} />,
  },
};


function StatisticNBA() {
  const [seasons, setSeasons] = useState([]);
  const [stages, setStages] = useState([]);
  const [homeaways, setHomeAway] = useState([]);
  const [teams, setTeams] = useState([]);
  const [players, setPlayers] = useState([]);
  const [opponents, setOpponents] = useState([]);

  const [filters, setFilters] = useState({});
  const [activeFilters, setActiveFilters] = useState([]);
  const [selectedFilterType, setSelectedFilterType] = useState(null);


  const [limitations, setLimitations] = useState(null); // ✅ обязательно null

  const [selectedLimitationType, setSelectedLimitationType] = useState(null);

  const [displayMode, setDisplayMode] = useState(null);

  const [statistic, setStatistic] = useState(null);

  const [answer, setAnswer] = useState("");

  document.title = `Гибкая статистика NBA`;


  // Взаимодействует с useFetchFilters.js
  useFetchFilters({
    filters,
    activeFilters,
    setTeams,
    setPlayers,
    setOpponents,
    setSeasons,
    setStages,
    setHomeAway,
  });


  // Взаимодействует с filterHandlers.js
  const {
    updateFilter,
    removeFilter,
    handleAddFilter,
    removeLimitation,
  } = createFilterHandlers(
    setFilters,
    setActiveFilters,
    setLimitations,
    setSelectedLimitationType
  );
 

  const handleSubmit = () => {
    const requestData = {
      ...filters,
      limitation: limitations
        ? `${limitations.count} ${limitations.direction}`
        : null,
      statistic: statistic || null, // ✅ передаем выбранное поле
      display: displayMode || null,
    };

    fetch("http://127.0.0.1:8000/api/nba/filterstat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        setAnswer(data.answer || []);
      })
      .catch((error) => console.error("Ошибка при отправке:", error));
  };


  const getThresholdHandler = (stat, setStatistic) => {
    if (!stat) return () => {};
  
    const model = stat.model;
    const fields = stat.fields || [];
  
    if (fields.includes("over_odds") || fields.includes("under_odds")) {
      return (e) => handleChangeOdds(e, setStatistic);
    }
  
    if (model === "NBAHandicapBet") {
      return (e) => handleChangeHandicap(e, setStatistic);
    }
  
    return (e) => handleChangeTotal(e, setStatistic);
  };

  const getThresholdBlurHandler = (stat, setStatistic) => {
    if (!stat) return () => {};
  
    const model = stat.model;
    const fields = stat.fields || [];
  
    if (fields.includes("over_odds") || fields.includes("under_odds")) {
      return (e) => blurOdds(e, setStatistic);
    }
    if (model === "NBAHandicapBet") {
      return (e) => blurHandicap(e, setStatistic);
    }
    return (e) => blurTotal(e, setStatistic);
  };
  


  // Взаимодействует с optionsLogic.js
  const availableFilterOptions = getAvailableFilterOptions(filterOptions, activeFilters);
  const availableLimitationOptions = getAvailableLimitationOptions(limitationOptions, limitations);
  const availableStatisticOptions = getAvailableStatisticOptions(statisticOptions, filters);
  const availableDisplayOptions = getAvailableDisplayOptions(displayOptions, statistic, limitations);


  return (
    <div>
      <Header />
      <main className="statistic-main">
      <div className="statistic-info">
          <div className="selectors">
            <div className="selector" style={{ width: "100%" }}>
              <label htmlFor="filter-type">Добавить фильтр</label>
              <div style={{ display: "flex", justifyContent: "center" }}>
                <Select
                  id="filter-type"
                  options={availableFilterOptions}
                  value={selectedFilterType}
                  onChange={(selected) => {
                    setSelectedFilterType(null);       // сбрасываем отображение
                    if (selected) handleAddFilter(selected.value); // сразу добавляем
                  }}
                  placeholder="Выберите параметр..."
                  styles={customMainSelectorStyles}
                />
              </div>
            </div>

            <div className="filter-group">
              {activeFilters.map((filterKey) => {
                const filter = filterRenderMap[filterKey];
                if (!filter) return null;

                return (
                  <div key={filterKey} className="selector">
                    <label>{filter.label}</label>
                    <div style={{ display: "flex", alignItems: "center" }}>
                      {filter.render({ filters, updateFilter, customSelectorStyles, teams, players, opponents, stages, seasons, homeaways })}
                      <button
                        className="delete-btn-selector"
                        onClick={() => removeFilter(filterKey)}
                      >
                        ×
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
            
            {Object.values(filters).some((v) => v) && (
              <>
                <div className="selector" style={{ width: "100%" }}>
                  <label htmlFor="limitation-type">Добавить ограничение</label>
                  <div style={{ display: "flex", justifyContent: "center" }}>
                    <Select
                      id="limitation-type"
                      options={availableLimitationOptions}
                      placeholder="Выберите ограничение..."
                      styles={customMainSelectorStyles}
                      isDisabled={!Object.values(filters).some((v) => v) || limitations}
                      onChange={(selectedOption) => {
                        if (!limitations && selectedOption) {
                          setLimitations({
                            direction: selectedOption.value, // ASC / DESC
                            count: 5, // значение по умолчанию
                          });
                        }
                      }}
                    />
                  </div>
                </div>

                {limitations && (
                  <div className="selector">
                    <label>
                      {limitations.direction === 'ASC'
                        ? `Первые ${limitations.count} матчей`
                        : `Последние ${limitations.count} матчей`}
                    </label>
                    <div style={{ display: 'flex', alignItems: 'center'}}>
                      <input
                        type="number"
                        min={1}
                        max={50}
                        value={limitations.count}
                        onChange={(e) => {
                          const val = parseInt(e.target.value, 10);
                          if (val >= 1 && val <= 50) {
                            setLimitations((prev) => ({
                              ...prev,
                              count: val,
                            }));
                          }
                        }}
                        className="input-limitation"
                      />
                      <button
                        className="delete-btn-selector"
                        onClick={() => removeLimitation(null)}
                      >
                        ×
                      </button>
                    </div>
                  </div>
                )}

                <div className="selector" style={{ width: "100%" }}>
                  <label htmlFor="statistic-type">Выбрать статистику (обязательное поле)</label>
                  <div style={{ display: "flex", justifyContent: "center" }}>
                    <Select
                      id="statistic-type"
                      options={availableStatisticOptions}
                      value={statistic?.label ? { label: statistic.label, value: statistic } : null}
                      onChange={(selectedOption) => {
                        setStatistic({
                          ...selectedOption.value,
                          label: selectedOption.label
                        });
                      }}
                      placeholder="Выберите статистику..."
                      styles={customMainSelectorStyles}
                      isDisabled={!Object.values(filters).some((v) => v)}
                    />
                  </div>

                  {statistic?.dynamicValue && (
                    <div style={{ marginTop: '10px' }}>
                      <input
                        id="threshold-input"
                        type="text"
                        inputMode="decimal"
                        value={statistic.threshold}
                        onChange={getThresholdHandler(statistic, setStatistic)}
                        onBlur={getThresholdBlurHandler(statistic, setStatistic)}
                        className="input-limitation"
                        style={{
                          borderRadius: '6px',
                          padding: '8px 12px',
                          fontSize: '16px',
                          width: '100%',
                          border: '1px solid #ccc',
                          outline: 'none',
                        }}
                      />
                    </div>
                  )}
                </div>


                <div className="selector" style={{ width: "100%" }}>
                  <label htmlFor="display-type">Отобразить как (обязательное поле)</label>
                  <div style={{ display: "flex", justifyContent: "center" }}>
                    <Select
                      id="display-type"
                      options={availableDisplayOptions}
                      value={availableDisplayOptions.find((opt) => opt.value === displayMode) || null}
                      onChange={(selected) => setDisplayMode(selected.value)}
                      placeholder="Отобразить как..."
                      styles={customMainSelectorStyles}
                      isDisabled={!Object.values(filters).some((v) => v)}
                    />
                  </div>
                </div>
              </>
            )}

          </div>

          <button className="submit-button" 
          onClick={handleSubmit}
          disabled={
            !Object.values(filters).some((v) => v) || !statistic || !displayMode
          }>
            Отправить
          </button>

          <div className="results">
            <h3>Результаты</h3>
            <strong>
              {Array.isArray(answer.statistic_display)
                ? answer.statistic_display.join(', ')
                : answer.statistic_display}
            </strong>

            {(
              !Object.values(filters).some((v) => v) ||
              !statistic ||
              !displayMode
            ) && (
              <div className="error-message" style={{ color: '#FF0000', marginTop: '8px' }}>
                Выберите параметры
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default StatisticNBA;
