import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom"; // ✅ Получаем параметры URL

import dayjs from "dayjs";
import "dayjs/locale/ru";
import Header from "../../components/Header";
import "../../styles/Schedule.css";

function ScheduleNBA() {
  const [matches, setMatches] = useState([]); // ✅ Изменил `null` на `[]`
  const [searchParams, setSearchParams] = useSearchParams(); // ✅ Хук для работы с query-параметрами

  const today = dayjs().format("YYYY-MM-DD");

  const dateParam = searchParams.get("date") || today;

  useEffect(() => {

    // ✅ Получаем параметр "date" из URL (например, ?date=2025-03-04)

    document.title = `Расписание ${dayjs(dateParam).format("DD.MM.YYYY")}`;

    fetch(`http://127.0.0.1:8000/api/nba/schedule/?date=${dateParam}`)
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
  return (
    <div>
      <Header />
      <main className="schedule-main">
        <div className="schedule-info">

          <div className="date-block">
            <button onClick={goToPreviousDay}>Назад</button>
            <p>{dayjs(dateParam).locale("ru").format("DD MMMM YYYY")}</p>
            <button onClick={goToNextDay}>Вперед</button>
          </div>

          {matches.length > 0 ? (
            matches.map((match) => {
              const homeScore = match.match_info.total.home_total;
              const awayScore = match.match_info.total.away_total;
              const homeWin = homeScore > awayScore;
              return (
                <Link to={`/nba/match/${match.match_id}`} key={match.match_id} className="match-item">
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

export default ScheduleNBA;
