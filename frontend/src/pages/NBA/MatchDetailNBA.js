import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNBA";
import "../../styles/MatchDetail.css";

function MatchDetailNBA() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nba/match/${id}`) // Загружаем данные о матче
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
                  <th>Стартер</th>
                  <th>PTS</th>
                  <th>FG</th>
                  <th>3PT</th>
                  <th>FT</th>
                  <th>OREB</th>
                  <th>DREV</th>
                  <th>REB</th>
                  <th>AST</th>
                  <th>STL</th>
                  <th>BLK</th>
                  <th>TO</th>
                  <th>PF</th>
                  <th>+/-</th>
                  <th>MIN</th>
                </tr>
              </thead>
              {match.match_info.home_starter_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.pts}</td>
                  <td>{p.fg}/{p.trying_fg}</td>
                  <td>{p.three_pt}/{p.attempted_three_pt}</td>
                  <td>{p.ft}/{p.trying_ft}</td>
                  <td>{p.oreb}</td>
                  <td>{p.dreb}</td>
                  <td>{p.reb}</td>
                  <td>{p.ast}</td>
                  <td>{p.stl}</td>
                  <td>{p.blk}</td>
                  <td>{p.turnovers}</td>
                  <td>{p.pf}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.min}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Скамейка</th>
                  <th>PTS</th>
                  <th>FG</th>
                  <th>3PT</th>
                  <th>FT</th>
                  <th>OREB</th>
                  <th>DREV</th>
                  <th>REB</th>
                  <th>AST</th>
                  <th>STL</th>
                  <th>BLK</th>
                  <th>TO</th>
                  <th>PF</th>
                  <th>+/-</th>
                  <th>MIN</th>
                </tr>
              </thead>
              {match.match_info.home_bench_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.pts}</td>
                  <td>{p.fg}/{p.trying_fg}</td>
                  <td>{p.three_pt}/{p.attempted_three_pt}</td>
                  <td>{p.ft}/{p.trying_ft}</td>
                  <td>{p.oreb}</td>
                  <td>{p.dreb}</td>
                  <td>{p.reb}</td>
                  <td>{p.ast}</td>
                  <td>{p.stl}</td>
                  <td>{p.blk}</td>
                  <td>{p.turnovers}</td>
                  <td>{p.pf}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.min}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th></th>
                  <th>{match.match_info.home_stat.fg}/{match.match_info.home_stat.trying_fg}</th>
                  <th>{match.match_info.home_stat.three_pt}/{match.match_info.home_stat.attempted_three_pt}</th>
                  <th>{match.match_info.home_stat.ft}/{match.match_info.home_stat.trying_ft}</th>
                  <th>{match.match_info.home_stat.oreb}</th>
                  <th>{match.match_info.home_stat.dreb}</th>
                  <th>{match.match_info.home_stat.reb}</th>
                  <th>{match.match_info.home_stat.ast}</th>
                  <th>{match.match_info.home_stat.stl}</th>
                  <th>{match.match_info.home_stat.blk}</th>
                  <th>{match.match_info.home_stat.turnovers}</th>
                  <th>{match.match_info.home_stat.pf}</th>
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
                  <th>Стартер</th>
                  <th>PTS</th>
                  <th>FG</th>
                  <th>3PT</th>
                  <th>FT</th>
                  <th>OREB</th>
                  <th>DREV</th>
                  <th>REB</th>
                  <th>AST</th>
                  <th>STL</th>
                  <th>BLK</th>
                  <th>TO</th>
                  <th>PF</th>
                  <th>+/-</th>
                  <th>MIN</th>
                </tr>
              </thead>
              {match.match_info.away_starter_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.pts}</td>
                  <td>{p.fg}/{p.trying_fg}</td>
                  <td>{p.three_pt}/{p.attempted_three_pt}</td>
                  <td>{p.ft}/{p.trying_ft}</td>
                  <td>{p.oreb}</td>
                  <td>{p.dreb}</td>
                  <td>{p.reb}</td>
                  <td>{p.ast}</td>
                  <td>{p.stl}</td>
                  <td>{p.blk}</td>
                  <td>{p.turnovers}</td>
                  <td>{p.pf}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.min}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>PTS</th>
                  <th>FG</th>
                  <th>3PT</th>
                  <th>FT</th>
                  <th>OREB</th>
                  <th>DREV</th>
                  <th>REB</th>
                  <th>AST</th>
                  <th>STL</th>
                  <th>BLK</th>
                  <th>TO</th>
                  <th>PF</th>
                  <th>+/-</th>
                  <th>MIN</th>
                </tr>
              </thead>
              {match.match_info.away_bench_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.pts}</td>
                  <td>{p.fg}/{p.trying_fg}</td>
                  <td>{p.three_pt}/{p.attempted_three_pt}</td>
                  <td>{p.ft}/{p.trying_ft}</td>
                  <td>{p.oreb}</td>
                  <td>{p.dreb}</td>
                  <td>{p.reb}</td>
                  <td>{p.ast}</td>
                  <td>{p.stl}</td>
                  <td>{p.blk}</td>
                  <td>{p.turnovers}</td>
                  <td>{p.pf}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.min}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Команда</th>
                  <th></th>
                  <th>{match.match_info.away_stat.fg}/{match.match_info.away_stat.trying_fg}</th>
                  <th>{match.match_info.away_stat.three_pt}/{match.match_info.away_stat.attempted_three_pt}</th>
                  <th>{match.match_info.away_stat.ft}/{match.match_info.away_stat.trying_ft}</th>
                  <th>{match.match_info.away_stat.oreb}</th>
                  <th>{match.match_info.away_stat.dreb}</th>
                  <th>{match.match_info.away_stat.reb}</th>
                  <th>{match.match_info.away_stat.ast}</th>
                  <th>{match.match_info.away_stat.stl}</th>
                  <th>{match.match_info.away_stat.blk}</th>
                  <th>{match.match_info.away_stat.turnovers}</th>
                  <th>{match.match_info.away_stat.pf}</th>
                </tr>
              </thead>
            </table>
          </div>
      </main>
    </div>
  );
}

export default MatchDetailNBA;
