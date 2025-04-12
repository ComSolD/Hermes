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
    { value: "graph", label: "Диаграмма" },
    { value: "boxplot", label: "Box Plot" },
  ];
  
  export const statisticOptions = [
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i1"] },
      label: "1-й Иннинг тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i2"] },
      label: "2-й Иннинг тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i3"] },
      label: "3-й Иннинг тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i4"] },
      label: "4-й Иннинг тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i1", "total_i2", "total_i3", "total_i4", "total_i5"] },
      label: "1-я Половина тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i6", "total_i7", "total_i8", "total_i9"] },
      label: "2-я Половина тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total"] },
      label: "Тотал команды",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i1", "total_i1_missed"] },
      label: "1-й Иннинг тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i2", "total_i2_missed"] },
      label: "2-й Иннинг тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i3", "total_i3_missed"] },
      label: "3-й Иннинг тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i4", "total_i4_missed"] },
      label: "4-й Иннинг тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i1", "total_i2", "total_i3", "total_i4", "total_i5", "total_i1_missed", "total_i2_missed", "total_i3_missed", "total_i4_missed", "total_i5_missed"] },
      label: "1-я Половина тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total_i6", "total_i7", "total_i8", "total_i9", "total_i6_missed", "total_i7_missed", "total_i8_missed", "total_i9_missed"] },
      label: "2-я Половина тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["total", "total_missed"] },
      label: "Тотал",
    },
    {
      value: { model: "MLBTeamPtsStat", fields: ["hit", "hit_missed"] },
      label: "Хиты",
    },
    {
      value: {
        model: "MLBMoneylineBet",
        fields: ["result"],
        aggregate: "full_time",
      },
      label: "Количество побед/поражений"
    },
    {
      value: {
        model: "MLBTotalBet",
        fields: ["total"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 8.5 // начальное значение
      },
      label: "Частота пробития общего тотала от букмекера"
    },
    {
      value: {
        model: "MLBTotalBet",
        fields: ["total"],
        aggregate: "1st_half",
        dynamicValue: true,
        threshold: 5 // начальное значение
      },
      label: "Частота пробития общего тотала от букмекера (с 1 по 5 иннинг)"
    },
    {
      value: {
        model: "MLBTotalBet",
        fields: ["total"],
        aggregate: "1st_inning",
        dynamicValue: true,
        threshold: 0.5 // начальное значение
      },
      label: "Частота пробития 1-го иннинга от букмекера"
    },
    {
      value: {
        model: "MLBTotalBet",
        fields: ["over_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Больше по котировке букмекера"
    },
    {
      value: {
        model: "MLBTotalBet",
        fields: ["under_odds"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 1.8 // начальное значение
      },
      label: "Меньше по котировке букмекера"
    },
    {
      value: {
        model: "MLBHandicapBet",
        fields: ["handicap"],
        aggregate: "full_time",
        dynamicValue: true,
        threshold: 0 // начальное значение
      },
      label: "Частота пробития форы от букмекера"
    },
    {
      value: { model: "MLBPlayerStat", fields: ["r"], aggregate: "player" },
      label: "Раны игрока",
    },
    {
      value: { model: "MLBPlayerStat", fields: ["h"], aggregate: "player" },
      label: "Хиты игрока",
    },
    {
      value: { model: "MLBPlayerStat", fields: ["avg"], aggregate: "player" },
      label: "AVG игрока",
    },
  ];
  
  export const limitationOptions = [
    { value: "DESC", label: "Последние N матчей" },
    { value: "ASC", label: "Первые N матчей" },
  ];