export const customMainSelectorStyles = {
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
      borderRadius: '6px', // Полный радиус для main-селекторов


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
      borderRadius: '6px',

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


export const customSelectorStyles = {
  // 🔸 стиль основного селектора
  ...customMainSelectorStyles,
  control: (provided, state) => ({
    ...customMainSelectorStyles.control(provided, state),
    borderTopLeftRadius: '6px',
    borderBottomLeftRadius: '6px',
    borderTopRightRadius: '0px',
    borderBottomRightRadius: '0px',
  }),
};