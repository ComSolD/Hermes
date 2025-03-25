import React, { useEffect, useState } from "react";
import Select from "react-select";

import Header from "../../components/Header";
import "../../styles/Statistic.css";

const filterOptions = [
  { value: "season", label: "Сезон" },
  { value: "stage", label: "Стадия" },
  { value: "team_id", label: "Команда" },
  { value: "opponent_id", label: "Оппонент" },
];

function StatisticNBA() {
  const [seasons, setSeasons] = useState([]);
  const [stages, setStages] = useState([]);
  const [teams, setTeams] = useState([]);
  const [opponents, setOpponents] = useState([]);

  const [filters, setFilters] = useState({});
  const [activeFilters, setActiveFilters] = useState([]);
  const [selectedFilterType, setSelectedFilterType] = useState(null);

  const [answer, setAnswer] = useState("");

  useEffect(() => {
    const isTeamActive = activeFilters.includes("team_id");

    if (isTeamActive) {
      fetch(`http://127.0.0.1:8000/api/nba/teams_by_filters/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(filters),
      })
        .then((res) => res.json())
        .then((data) => setTeams(data.teams || []))
        .catch((err) => console.error("Ошибка загрузки команд:", err));
      }
    }, [filters, activeFilters]);

    useEffect(() => {
      const isOpponentActive = activeFilters.includes("opponent_id");
  
      if (isOpponentActive) {
        fetch(`http://127.0.0.1:8000/api/nba/opponents_by_filters/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(filters),
        })
          .then((res) => res.json())
          .then((data) => setOpponents(data.opponents || []))
          .catch((err) => console.error("Ошибка загрузки команд:", err));
        }
      }, [filters, activeFilters]);

    useEffect(() => {
      const isSeasonActive = activeFilters.includes("season");
    
      if (isSeasonActive) {
        fetch("http://127.0.0.1:8000/api/nba/seasons_by_filters/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(filters),
        })
          .then((res) => res.json())
          .then((data) => setSeasons(data.seasons || []))
          .catch((err) => console.error("Ошибка загрузки сезонов:", err));
      }
    }, [filters, activeFilters]);

    useEffect(() => {
      const isStageActive = activeFilters.includes("stage");
    
      if (isStageActive) {
        fetch("http://127.0.0.1:8000/api/nba/stages_by_filters/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(filters),
        })
          .then((res) => res.json())
          .then((data) => setStages(data.stages || []))
          .catch((err) => console.error("Ошибка загрузки сезонов:", err));
      }
    }, [filters, activeFilters]);




  const updateFilter = (key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const removeFilter = (key) => {
    setActiveFilters((prev) => prev.filter((item) => item !== key));
    setFilters((prev) => {
      const newFilters = { ...prev };
      delete newFilters[key];
      return newFilters;
    });
  };

  const handleAddFilter = () => {
    if (selectedFilterType && !activeFilters.includes(selectedFilterType.value)) {
      setActiveFilters((prev) => [...prev, selectedFilterType.value]);
      setSelectedFilterType(null);
    }
  };



  const handleSubmit = () => {
    fetch("http://127.0.0.1:8000/api/nba/filterstat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filters),
    })
      .then((response) => response.json())
      .then((data) => {
        setAnswer(data.answer || []);
      })
      .catch((error) => console.error("Ошибка при отправке:", error));
  };


  const customStyles = {
    container: (provided) => ({
      ...provided,
      width: '100%', // 🔹 растягиваем весь селект по ширине
      flex: 1,
    }),
    control: (provided, state) => ({
      ...provided,
      backgroundColor: '#fff',
      borderColor: state.isFocused ? '#36c' : '#ccc',
      boxShadow: state.isFocused
        ? '0 0 0 2px rgba(51, 102, 204, 0.3)'
        : 'none',
      borderTopLeftRadius: '6px',
      borderBottomLeftRadius: '6px',
      borderTopRightRadius: '0px',
      borderBottomRightRadius: '0px',

      minHeight: '42px',
      fontSize: '16px',
      paddingLeft: '6px',
      paddingRight: '6px',
      transition: 'border-color 0.2s, box-shadow 0.2s',
      cursor: 'pointer',
    }),
    option: (provided, state) => {
      const isSelected = state.isSelected;
      const isFocused = state.isFocused;
    
      return {
        ...provided,
        backgroundColor: isSelected
          ? isFocused
            ? '#2a57aa' // 🔹 выделено и наведено — чуть темнее
            : '#36c'    // 🔹 просто выбрано
          : isFocused
          ? 'rgba(51, 102, 204, 0.1)' // 🔹 просто наведение
          : '#fff',                   // 🔸 обычный
    
        color: isSelected ? '#fff' : '#333',
        fontWeight: isSelected ? 'bold' : 'normal',
    
        padding: '10px 12px',
        fontSize: '15px',
        cursor: 'pointer',
        transition: 'background-color 0.2s, color 0.2s',
      };
    },
    menu: (provided) => ({
      ...provided,
      zIndex: 9999,
      borderTopLeftRadius: '6px',
      borderBottomLeftRadius: '6px',
      borderTopRightRadius: '0px',
      borderBottomRightRadius: '0px',

      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
      overflow: 'hidden',
    }),
    singleValue: (provided) => ({
      ...provided,
      color: '#333',
      fontWeight: 500,
    }),
    input: (provided) => ({
      ...provided,
      color: '#333',
      fontSize: '16px',
    }),
    placeholder: (provided) => ({
      ...provided,
      color: '#888',
      fontSize: '15px',
    }),
  };






  const TeamSelector = () => {
    const options = teams.map((team) => ({
      value: team.team_id,
      label: team.name,
    }));
  
    const currentValue = options.find((opt) => opt.value === filters.team_id) || null;
  
    return (
      <Select
        options={[{ value: "", label: "Все команды" }, ...options]}
        value={currentValue}
        onChange={(selectedOption) => updateFilter("team_id", selectedOption?.value || "")}
        placeholder="Выберите команду..."
        styles={customStyles}
        isSearchable
        isDisabled={options.length === 0}  // 🔹 отключаем пока нет данных
      />
    );
  };


  const OpponentSelector = () => {
    const options = opponents.map((opponent) => ({
      value: opponent.team_id,
      label: opponent.name,
    }));
  
    const currentValue = options.find((opt) => opt.value === filters.opponent_id) || null;
  
    return (
      <Select
        options={[{ value: "", label: "Все оппоненты" }, ...options]}
        value={currentValue}
        onChange={(selectedOption) => updateFilter("opponent_id", selectedOption?.value || "")}
        placeholder="Выберите оппонента..."
        styles={customStyles}
        isSearchable
        isDisabled={options.length === 0}  // 🔹 отключаем пока нет данных
      />
    );
  };


  const StageSelector = () => {
    const options = stages.map((stage) => ({
      value: stage.value,
      label: stage.label,
    }));
  
    const currentValue = options.find((opt) => opt.value === filters.stage) || null;
  
    return (
      <Select
        options={[{ value: "", label: "Все стадии" }, ...options]}
        value={currentValue}
        onChange={(selected) => updateFilter('stage', selected?.value || '')}
        placeholder="Выберите стадию..."
        isSearchable
        isDisabled={options.length === 0}
        styles={customStyles}
        classNamePrefix="custom-select"
      />
    );
  };


  const SeasonSelector = () => {
    const options = seasons.map((season) => ({
      value: season,
      label: season,
    }));
  
    const currentValue = options.find((opt) => opt.value === filters.season) || null;
  
    return (
      <Select
        options={[{ value: "", label: "Все сезоны" }, ...options]}
        value={currentValue}
        onChange={(selected) => updateFilter('season', selected?.value || '')}
        placeholder="Выберите сезон..."
        isSearchable
        isDisabled={options.length === 0}
        styles={customStyles}
        classNamePrefix="custom-select"
      />
    );
  };





  const isTeamSelected = activeFilters.includes("team_id");

  const availableFilterOptions = filterOptions.filter((opt) => {
    // Убираем уже выбранные
    if (activeFilters.includes(opt.value)) return false;

    // opponent_id можно выбрать только если выбрана команда
    if (opt.value === "opponent_id" && !isTeamSelected) return false;

    return true;
  });




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
                  onChange={setSelectedFilterType}
                  placeholder="Выберите параметр..."
                  styles={customStyles}
                />
                <button onClick={handleAddFilter}>+</button>
              </div>
            </div>

            <div className="filter-group">
              {activeFilters.includes("season") && (
                <div className="selector">
                  <label htmlFor="season-select">Сезон</label>
                  <div style={{ display: "flex", alignItems: "center"  }}>
                    <SeasonSelector />
                    <button onClick={() => removeFilter("season")}>×</button>
                  </div>
                </div>
              )}

              {activeFilters.includes("stage") && (
                <div className="selector">
                  <label htmlFor="stage-select">Стадия</label>
                  <div style={{ display: "flex", alignItems: "center"  }}>
                    <StageSelector />
                    <button onClick={() => removeFilter("stage")}>×</button>
                  </div>
                </div>
              )}

              {activeFilters.includes("team_id") && (
                <div className="selector">
                  <label htmlFor="team-select">Команда</label>
                  <div style={{ display: "flex", alignItems: "center" }}>
                    <TeamSelector />
                    <button onClick={() => removeFilter("team_id")}>×</button>
                  </div>
                </div>
              )}

              {activeFilters.includes("opponent_id") && (
                <div className="selector">
                  <label htmlFor="opponent-select">Оппоненты</label>
                  <div style={{ display: "flex", alignItems: "center" }}>
                    <OpponentSelector />
                    <button onClick={() => removeFilter("opponent_id")}>×</button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <button className="submit-button" onClick={handleSubmit}>
            Отправить
          </button>

          <div className="results">
            <h3>Результаты</h3>
            <strong>{answer.total_matches}</strong>
          </div>
        </div>
      </main>
    </div>
  );
}

export default StatisticNBA;
