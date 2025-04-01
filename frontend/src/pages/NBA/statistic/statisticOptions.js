export const filterOptions = [
    { value: "season", label: "Сезон" },
    { value: "stage", label: "Стадия" },
    { value: "homeaway", label: "Положение команды" },
    { value: "team_id", label: "Команда" },
    { value: "player_id", label: "Игрок" },
    { value: "opponent_id", label: "Оппонент" },
  ];
  
  export const displayOptions = [
    { value: "avg", label: "AVG" },
    { value: "list", label: "Список" },
  ];
  
  export const statisticOptions = [
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q1"] },
      label: "1-я Четверть тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q2"] },
      label: "2-я Четверть тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q3"] },
      label: "3-я Четверть тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q4"] },
      label: "4-я Четверть тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total"] },
      label: "Тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q1", "total_q1_missed"] },
      label: "1-я Четверть тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total", "total_missed"] },
      label: "Тотал",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["ast"], aggregate: "team" },
      label: "Передачи команды",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["ast"], aggregate: "player" },
      label: "Передачи игрока",
    },
  ];
  
  export const limitationOptions = [
    { value: "DESC", label: "Последние N матчей" },
    { value: "ASC", label: "Первые N матчей" },
  ];