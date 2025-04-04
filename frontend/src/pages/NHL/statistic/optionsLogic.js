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
      if (model === "NHLPlayerStat" && aggregate === "player") {
        return Boolean(filters.player_id);
      }
      if (model === "NHLTeamPtsStat") {
        return Boolean(filters.team_id);
      }
      if (model === "NHLTotalBet") {
        return Boolean(filters.team_id);
      }
      if (model === "NHLHandicapBet") {
        return Boolean(filters.team_id);
      }
      if (model === "NHLMoneylineBet") {
        return Boolean(filters.team_id);
      }
      if (model === "NHLPlayerStat" && aggregate === "team") {
        return Boolean(filters.team_id);
      }
      return true;
    });
  };

  export const getAvailableDisplayOptions = (displayOptions, statistic, limitations) => {
    return displayOptions.filter((opt) => {
      if (opt.value === "overdrawunder") {
        return statistic?.model === "NHLTotalBet";
      }

      if (opt.value === "windrawlose") {
        return (
          statistic?.model === "NHLHandicapBet" ||
          statistic?.model === "NHLMoneylineBet"
        );
      }

      if (opt.value === "avg") {
        return (
          statistic?.model === "NHLTeamPtsStat" ||
          statistic?.model === "NHLPlayerStat"
        );
      }

      if (opt.value === "list") {
        return Boolean(limitations); // Показываем только если ограничение выбрано
      }
      return true;
    });
  };
  