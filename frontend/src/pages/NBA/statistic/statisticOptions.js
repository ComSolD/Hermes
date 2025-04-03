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
    { value: "overdrawunder", label: "Больше/Равно/Меньше" },
    { value: "windrawlose", label: "Победа/Ничья/Поражение" },
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
      value: { model: "NBATeamPtsStat", fields: ["total_q1", "total_q2"] },
      label: "1-я Половина тотал команды",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q3", "total_q4"] },
      label: "2-я Половина тотал команды",
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
      value: { model: "NBATeamPtsStat", fields: ["total_q2", "total_q2_missed"] },
      label: "2-я Четверть тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q3", "total_q3_missed"] },
      label: "3-я Четверть тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q4", "total_q4_missed"] },
      label: "4-я Четверть тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q1", "total_q2", "total_q1_missed", "total_q2_missed"] },
      label: "1-я Половина тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total_q3", "total_q4", "total_q3_missed", "total_q4_missed"] },
      label: "2-я Половина тотал",
    },
    {
      value: { model: "NBATeamPtsStat", fields: ["total", "total_missed"] },
      label: "Тотал",
    },
    {
      value: {
        model: "NBAMoneylineBet",
        fields: ["result"],
        aggregate: "full_time",
      },
      label: "Количество побед/поражений"
    },
    {
      value: {
        model: "NBATotalBet",
        fields: ["total"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 200 // начальное значение
      },
      label: "Частота пробития общего тотала от букмекера"
    },
    {
      value: {
        model: "NBATotalBet",
        fields: ["over_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Больше по котировке букмекера"
    },
    {
      value: {
        model: "NBATotalBet",
        fields: ["under_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Меньше по котировке букмекера"
    },
    {
      value: {
        model: "NBAHandicapBet",
        fields: ["handicap"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 0 // начальное значение
      },
      label: "Частота пробития форы от букмекера"
    },
    {
      value: { model: "NBAPlayerStat", fields: ["three_pt"], aggregate: "team" },
      label: "Трехочковые команды",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["reb"], aggregate: "team" },
      label: "Подборы команды",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["ast"], aggregate: "team" },
      label: "Передачи команды",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["pts"], aggregate: "player" },
      label: "Очки игрока",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["three_pt"], aggregate: "player" },
      label: "Трехочковые игрока",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["reb"], aggregate: "player" },
      label: "Подборы игрока",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["ast"], aggregate: "player" },
      label: "Передачи игрока",
    },
    {
      value: { model: "NBAPlayerStat", fields: ["plus_minus"], aggregate: "player" },
      label: "+/- игрока",
    },
  ];
  
  export const limitationOptions = [
    { value: "DESC", label: "Последние N матчей" },
    { value: "ASC", label: "Первые N матчей" },
  ];