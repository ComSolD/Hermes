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


  export const handleChangeTotal = (e, setStatistic) => {
    const raw = e.target.value.replace(',', '.');
  
    // Разрешаем ввод чисел с . или .5, включая временные состояния вроде "12."
    const isValid = /^(\d+)?([.]5?)?$/.test(raw);
  
    if (!isValid) return;
  
    const num = parseFloat(raw);
    if (!isNaN(num) && num >= 1 && num <= 50) {
      setStatistic((prev) => ({
        ...prev,
        threshold: raw,
      }));
    }
  };

  export const handleChangeHandicap = (e, setStatistic) => {
    const raw = e.target.value.replace(',', '.');
  
    const isValid = /^-?(\d+)?([.]5?)?$/.test(raw);
  
    if (!isValid) return;
  
    const num = parseFloat(raw);
    if (!isNaN(num) && num >= -50 && num <= 50) {
      setStatistic((prev) => ({
        ...prev,
        threshold: raw,
      }));
    }
  };

export const handleChangeOdds = (e, setStatistic) => {
  const raw = e.target.value.replace(',', '.');
  const isValid = /^\d+(\.\d{0,1})?$/.test(raw); // до 1 знака после точки

  if (!isValid) return;

  const num = parseFloat(raw);
  if (num >= 1.1 && num <= 11.0) {
    setStatistic((prev) => ({
      ...prev,
      threshold: raw,
    }));
  }
};

export const blurTotal = (e, setStatistic) => {
  const val = e.target.value.replace(',', '.');
  const num = parseFloat(val);

  if (!isNaN(num)) {
    const fixed = Math.round(num * 2) / 2;
    const clamped = Math.max(1, Math.min(50, fixed));

    setStatistic((prev) => ({
      ...prev,
      threshold: clamped.toString(),
    }));
  } else {
    setStatistic((prev) => ({ ...prev, threshold: '0' }));
  }
};

export const blurHandicap = (e, setStatistic) => {
  const val = e.target.value.replace(',', '.');
  const num = parseFloat(val);

  if (!isNaN(num)) {
    const fixed = Math.round(num * 2) / 2;
    const clamped = Math.max(-50, Math.min(50, fixed));

    setStatistic((prev) => ({
      ...prev,
      threshold: clamped.toString(),
    }));
  } else {
    setStatistic((prev) => ({ ...prev, threshold: '0' }));
  }
};

export const blurOdds = (e, setStatistic) => {
  const val = e.target.value.replace(',', '.');
  const num = parseFloat(val);

  if (!isNaN(num)) {
    const fixed = Math.round(num * 10) / 10; // 1 знак после запятой
    const clamped = Math.max(1.1, Math.min(11.0, fixed));

    setStatistic((prev) => ({
      ...prev,
      threshold: clamped.toString(),
    }));
  } else {
    setStatistic((prev) => ({ ...prev, threshold: '1.1' }));
  }
};
