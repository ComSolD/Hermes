export const createFilterHandlers = (
    setFilters,
    setActiveFilters,
    setLimitations,
    setSelectedLimitationType
  ) => {
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
  
    const handleAddFilter = (filterKey) => {
      if (filterKey && typeof filterKey === "string") {
        setActiveFilters((prev) =>
          prev.includes(filterKey) ? prev : [...prev, filterKey]
        );
      }
    };
  
    const removeLimitation = () => {
      setLimitations(null);
      setSelectedLimitationType(null);
    };
  
    return {
      updateFilter,
      removeFilter,
      handleAddFilter,
      removeLimitation,
    };
  };