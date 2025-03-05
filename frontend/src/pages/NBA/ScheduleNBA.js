import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom"; // ✅ Получаем параметры URL
import { Link } from "react-router-dom";

import dayjs from "dayjs";
import Header from "../../components/Header";
import "../../styles/Schedule.css";

function ScheduleNBA() {
  const [matches, setMatches] = useState([]); // ✅ Изменил `null` на `[]`
  const [searchParams] = useSearchParams(); // ✅ Хук для работы с query-параметрами

  useEffect(() => {
    const today = dayjs().format("YYYY-MM-DD");

    // ✅ Получаем параметр "date" из URL (например, ?date=2025-03-04)
    const dateParam = searchParams.get("date") || today;

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
  }, [searchParams]); // ✅ Запрос обновляется при изменении `date` в URL

  return (
    <div>
      <Header />
      <main className="schedule-main">
        <div className="schedule-info">
          <h1>Расписание</h1>
          <p>Выбранная дата: {dayjs(searchParams).format("DD.MM.YYYY")}</p>

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
