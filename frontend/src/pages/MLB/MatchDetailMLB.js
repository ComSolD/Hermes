import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderMLB";
import "../../styles/MatchDetail.css";

function MatchDetailMLB() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/mlb/match/${id}`) // Загружаем данные о матче
      .then((response) => response.json())
      .then((data) => {
        setMatch(data)
        document.title = `${data.match_info.home_team} vs ${data.match_info.away_team}`;
      })
      .catch((error) => console.error("Ошибка загрузки:", error));


  }, [id]);

  if (!match) {
    return (
      <div>
        <Header />
        <h1 style={{textAlign: "center"}}>Загрузка...</h1>
      </div>
    );
  }

  return (

    <div>
      <Header />
      <main className="match-main">
        <MatchHeader match={match} id={id} />
        
        {/* Нижние два блока */}
          {/* Блок 1 - Инфа о первой команде */}
          <div className="block-info">
            <div className="team-name-cell">
              <img src={match.match_info.home_team_logo || '/default_logo.png'} alt="logo" className="team-logo-stat" />
              <h1>{match.match_info.home_team}</h1>
            </div>
            <table className="stat-info">
              <colgroup>
                <col style={{ width: '150px' }} />
              </colgroup>
              <thead>
                <tr>
                  <th>Бьющий</th>
                  <th>AB</th>
                  <th>R</th>
                  <th>H</th>
                  <th>RBI</th>
                  <th>HR</th>
                  <th>BB</th>
                  <th>K</th>
                  <th>AVG</th>
                  <th>OBP</th>
                  <th>SLG</th>
                </tr>
              </thead>
              {match.match_info.home_hitter_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.ab}</td>
                  <td>{p.r}</td>
                  <td>{p.h}</td>
                  <td>{p.rbi}</td>
                  <td>{p.hr}</td>
                  <td>{p.bb}</td>
                  <td>{p.k}</td>
                  <td>{p.avg}</td>
                  <td>{p.obp}</td>
                  <td>{p.slg}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th>{match.match_info.home_stat_hitter.ab}</th>
                  <th>{match.match_info.home_stat_hitter.r}</th>
                  <th>{match.match_info.home_stat_hitter.h}</th>
                  <th>{match.match_info.home_stat_hitter.rbi}</th>
                  <th>{match.match_info.home_stat_hitter.hr}</th>
                  <th>{match.match_info.home_stat_hitter.bb}</th>
                  <th>{match.match_info.home_stat_hitter.k}</th>
                </tr>
              </thead>
              <thead>
                <tr>
                  <th>Подающий</th>
                  <th>IP</th>
                  <th>H</th>
                  <th>R</th>
                  <th>ER</th>
                  <th>BB</th>
                  <th>K</th>
                  <th>HR</th>
                  <th>PC-ST</th>
                  <th>ERA</th>
                </tr>
              </thead>
              {match.match_info.home_pitcher_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.ip}</td>
                  <td>{p.h}</td>
                  <td>{p.r}</td>
                  <td>{p.er}</td>
                  <td>{p.bb}</td>
                  <td>{p.k}</td>
                  <td>{p.hr}</td>
                  <td>{p.pc}/{p.st}</td>
                  <td>{p.era}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th>{match.match_info.home_stat_pitcher.ip}</th>
                  <th>{match.match_info.home_stat_pitcher.h}</th>
                  <th>{match.match_info.home_stat_pitcher.r}</th>
                  <th>{match.match_info.home_stat_pitcher.er}</th>
                  <th>{match.match_info.home_stat_pitcher.bb}</th>
                  <th>{match.match_info.home_stat_pitcher.k}</th>
                  <th>{match.match_info.home_stat_pitcher.hr}</th>
                  <th>{match.match_info.home_stat_pitcher.pc}/{match.match_info.home_stat_pitcher.st}</th>
                </tr>
              </thead>
            </table>

           
          </div>

          {/* Блок 2 - Инфа о второй команде */}
          <div className="block-info">
            <div className="team-name-cell">
              <img src={match.match_info.away_team_logo || '/default_logo.png'} alt="logo" className="team-logo-stat" />
              <h1>{match.match_info.away_team}</h1>
            </div>
            <table className="stat-info">
              <colgroup>
                <col style={{ width: '150px' }} />
              </colgroup>
              <thead>
                <tr>
                  <th>Бьющий</th>
                  <th>AB</th>
                  <th>R</th>
                  <th>H</th>
                  <th>RBI</th>
                  <th>HR</th>
                  <th>BB</th>
                  <th>K</th>
                  <th>AVG</th>
                  <th>OBP</th>
                  <th>SLG</th>
                </tr>
              </thead>
              {match.match_info.away_hitter_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.ab}</td>
                  <td>{p.r}</td>
                  <td>{p.h}</td>
                  <td>{p.rbi}</td>
                  <td>{p.hr}</td>
                  <td>{p.bb}</td>
                  <td>{p.k}</td>
                  <td>{p.avg}</td>
                  <td>{p.obp}</td>
                  <td>{p.slg}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th>{match.match_info.away_stat_hitter.ab}</th>
                  <th>{match.match_info.away_stat_hitter.r}</th>
                  <th>{match.match_info.away_stat_hitter.h}</th>
                  <th>{match.match_info.away_stat_hitter.rbi}</th>
                  <th>{match.match_info.away_stat_hitter.hr}</th>
                  <th>{match.match_info.away_stat_hitter.bb}</th>
                  <th>{match.match_info.away_stat_hitter.k}</th>
                </tr>
              </thead>
              <thead>
                <tr>
                  <th>Подающий</th>
                  <th>IP</th>
                  <th>H</th>
                  <th>R</th>
                  <th>ER</th>
                  <th>BB</th>
                  <th>K</th>
                  <th>HR</th>
                  <th>PC-ST</th>
                  <th>ERA</th>
                </tr>
              </thead>
              {match.match_info.away_pitcher_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.ip}</td>
                  <td>{p.h}</td>
                  <td>{p.r}</td>
                  <td>{p.er}</td>
                  <td>{p.bb}</td>
                  <td>{p.k}</td>
                  <td>{p.hr}</td>
                  <td>{p.pc}/{p.st}</td>
                  <td>{p.era}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th>{match.match_info.away_stat_pitcher.ip}</th>
                  <th>{match.match_info.away_stat_pitcher.h}</th>
                  <th>{match.match_info.away_stat_pitcher.r}</th>
                  <th>{match.match_info.away_stat_pitcher.er}</th>
                  <th>{match.match_info.away_stat_pitcher.bb}</th>
                  <th>{match.match_info.away_stat_pitcher.k}</th>
                  <th>{match.match_info.away_stat_pitcher.hr}</th>
                  <th>{match.match_info.away_stat_pitcher.pc}/{match.match_info.away_stat_pitcher.st}</th>
                </tr>
              </thead>
            </table>
          </div>
      </main>
    </div>
  );
}

export default MatchDetailMLB;
