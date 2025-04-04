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
      value: { model: "NHLTeamPtsStat", fields: ["total_p1"] },
      label: "1-я Четверть тотал команды",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total_p2"] },
      label: "2-я Четверть тотал команды",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total_p3"] },
      label: "3-я Четверть тотал команды",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total"] },
      label: "Тотал команды",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total_p1", "total_p1_missed"] },
      label: "1-я Четверть тотал",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total_p2", "total_p2_missed"] },
      label: "2-я Четверть тотал",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total_p3", "total_p3_missed"] },
      label: "3-я Четверть тотал",
    },
    {
      value: { model: "NHLTeamPtsStat", fields: ["total", "total_missed"] },
      label: "Тотал",
    },
    {
      value: {
        model: "NHLMoneylineBet",
        fields: ["result"],
        aggregate: "full_time",
      },
      label: "Количество побед/поражений"
    },
    {
      value: {
        model: "NHLTotalBet",
        fields: ["total"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 6 // начальное значение
      },
      label: "Частота пробития общего тотала от букмекера"
    },
    {
      value: {
        model: "NHLTotalBet",
        fields: ["over_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Больше по котировке букмекера"
    },
    {
      value: {
        model: "NHLTotalBet",
        fields: ["under_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Меньше по котировке букмекера"
    },
    {
      value: {
        model: "NHLHandicapBet",
        fields: ["handicap"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 0 // начальное значение
      },
      label: "Частота пробития форы от букмекера"
    },
    {
      value: { model: "NHLPlayerStat", fields: ["g"], aggregate: "player" },
      label: "Шайб игрока",
    },
  ];
  
  export const limitationOptions = [
    { value: "DESC", label: "Последние N матчей" },
    { value: "ASC", label: "Первые N матчей" },
  ];