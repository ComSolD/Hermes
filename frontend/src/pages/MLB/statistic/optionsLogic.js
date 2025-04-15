export const getAvailableFilterOptions = (filterOptions, activeFilters) => {
    const isTeamSelected = activeFilters.includes("team_id");
  
    return filterOptions.filter((opt) => {
      if (activeFilters.includes(opt.value)) return false;
      if (opt.value === "opponent_id" && !isTeamSelected) return false;
      return true;
    });
  };
  
  export const getAvailableLimitationOptions = (limitationOptions, limitations) => {
    return limitationOptions.filter(
      (opt) => !limitations || opt.value !== limitations.value
    );
  };
  
  export const getAvailableStatisticOptions = (statisticOptions, filters) => {
    return statisticOptions.filter((opt) => {
      const { model, aggregate } = opt.value;
      if (model === "MLBPlayerStat" && aggregate === "player") {
        return Boolean(filters.player_id);
      }
      if (model === "MLBTeamPtsStat") {
        return Boolean(filters.team_id);
      }
      if (model === "MLBTotalBet") {
        return Boolean(filters.team_id);
      }
      if (model === "MLBHandicapBet") {
        return Boolean(filters.team_id);
      }
      if (model === "MLBMoneylineBet") {
        return Boolean(filters.team_id);
      }
      if (model === "MLBPlayerStat" && aggregate === "team") {
        return Boolean(filters.team_id);
      }
      return true;
    });
  };

  export const getAvailableDisplayOptions = (displayOptions, statistic, limitations) => {
    return displayOptions.filter((opt) => {
      if (opt.value === "overdrawunder") {
        return statistic?.model === "MLBTotalBet";
      }

      if (opt.value === "windrawlose") {
        return (
          statistic?.model === "MLBHandicapBet" ||
          statistic?.model === "MLBMoneylineBet"
        );
      }

      if (opt.value === "avg") {
        return (
          statistic?.model === "MLBTeamPtsStat" ||
          statistic?.model === "MLBPlayerStat"
        );
      }

      if (opt.value === "list") {
        return Boolean(limitations); // Показываем только если ограничение выбрано
      }

      if (opt.value === "graph") {
        return (
          (statistic?.model === "MLBTeamPtsStat" ||
          statistic?.model === "MLBPlayerStat") &&
          Boolean(limitations)
        );
      }

      if (opt.value === "boxplot") {
        return (
          (statistic?.model === "MLBTeamPtsStat" ||
          statistic?.model === "MLBPlayerStat")
        );
      }

      return true;
    });
  };
  