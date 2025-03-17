import { useEffect, useState, useRef } from "react";
import { useSearchParams, Link } from "react-router-dom"; // ✅ Получаем параметры URL

import dayjs from "dayjs";
import "dayjs/locale/ru";

import ReactDatePicker, { registerLocale } from "react-datepicker";
import ru from "date-fns/locale/ru"; // Локализация

import Header from "../../components/Header";
import "../../styles/Schedule.css";

const ruLocale = {
  ...ru,
  options: {
    ...ru.options,
    weekStartsOn: 1, // ✅ Неделя начинается с понедельника
  },
};
registerLocale("ru", ruLocale);

function ScheduleMLB() {
  const [matches, setMatches] = useState([]); // ✅ Изменил `null` на `[]`
  const [searchParams, setSearchParams] = useSearchParams(); // ✅ Хук для работы с query-параметрами
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const calendarRef = useRef(null);

  const today = dayjs().format("YYYY-MM-DD");

  const dateParam = searchParams.get("date") || today;

  useEffect(() => {

    // ✅ Получаем параметр "date" из URL (например, ?date=2025-03-04)

    document.title = `Расписание ${dayjs(dateParam).format("DD.MM.YYYY")}`;

    fetch(`http://127.0.0.1:8000/api/mlb/schedule/?date=${dateParam}`)
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) { // ✅ Проверяем, пришёл ли массив матчей
          setMatches(data);
        } else {
          setMatches([]); // ✅ Если ошибка или пустые данные, сбрасываем
        }
      })
      .catch((error) => {
        console.error("Ошибка загрузки:", error);
        setMatches([]);
      });
  }, [dateParam]); // ✅ Запрос обновляется при изменении `date` в URL

  const goToPreviousDay = () => {
    const prevDay = dayjs(dateParam).subtract(1, "day").format("YYYY-MM-DD");
    setSearchParams({ date: prevDay });
  };

  const goToNextDay = () => {
    const nextDay = dayjs(dateParam).add(1, "day").format("YYYY-MM-DD");
    setSearchParams({ date: nextDay });
  };

  const handleDateChange = (date) => {
    const formattedDate = dayjs(date).format("YYYY-MM-DD");
    setSearchParams({ date: formattedDate });
    setIsCalendarOpen(false); // Закрываем календарь после выбора даты
  };

  useEffect(() => {
    function handleClickOutside(event) {
      if (calendarRef.current && !calendarRef.current.contains(event.target)) {
        setIsCalendarOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div>
      <Header />
      <main className="schedule-main">
        <div className="schedule-info">

          <div className="date-block">
            <button onClick={goToPreviousDay}>Назад</button>

            <div className="date-picker-wrapper" ref={calendarRef}>
              <p onClick={() => setIsCalendarOpen(!isCalendarOpen)} className="date-text">
                {dayjs(dateParam).locale("ru").format("DD MMMM YYYY")}
              </p>
              {isCalendarOpen && (
                <div className="calendar-container">
                  <ReactDatePicker
                    selected={dayjs(dateParam).toDate()}
                    onChange={handleDateChange}
                    dateFormat="dd MMMM yyyy"
                    locale="ru"
                    inline
                    fixedWeeks
                    showWeekNumbers={false}
                    className="custom-calendar"
                    dayClassName={(date) => {
                      const day = dayjs(date).day();
                      return day === 0 || day === 6 ? "weekend" : "";
                    }}
                    renderCustomHeader={({
                      date,
                      decreaseMonth,
                      increaseMonth,
                      prevMonthButtonDisabled,
                      nextMonthButtonDisabled,
                    }) => (
                      <div className="custom-header">
                        <button onClick={decreaseMonth} disabled={prevMonthButtonDisabled}>
                          Назад
                        </button>
                        <button onClick={increaseMonth} disabled={nextMonthButtonDisabled}>
                          Вперед
                        </button>
                      </div>
                    )}
                    showMonthYearDropdown={false}
                  />

                </div>
              )}
            </div>
            
            <button onClick={goToNextDay}>Вперед</button>
          </div>

          {matches.length > 0 ? (
            matches.map((match) => {
              const homeScore = match.match_info.total.home_total;
              const awayScore = match.match_info.total.away_total;
              const homeWin = homeScore > awayScore;
              return (
                <Link to={`/mlb/match/${match.match_id}`} key={match.match_id} className="match-item">
                  <span className={homeWin ? "winner" : "loser"}>
                    {match.match_info.home_team}
                  </span>
                  <span className="match-score">
                    {homeScore}:{awayScore}
                  </span>
                  <span className={!homeWin ? "winner" : "loser"}>
                    {match.match_info.away_team}
                  </span>
                </Link>
              );
            })
          ) : (
            <p>Матчи не найдены</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default ScheduleMLB;
