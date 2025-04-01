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
      if (model === "NBAPlayerStat" && aggregate === "player") {
        return Boolean(filters.player_id);
      }
      return true;
    });
  };

  export const getAvailableDisplayOptions = (displayOptions, statistic) => {
    return displayOptions.filter((opt) => {
      if (opt.value === "overdrawunder") {
        return statistic?.model === "NBATotalBet";
      }
      return true;
    });
  };
  