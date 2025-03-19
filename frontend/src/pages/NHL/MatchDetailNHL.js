import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../../components/Header";
import MatchHeader from "./MatchHeaderNHL";
import "../../styles/MatchDetail.css";

function MatchDetailNHL() {
  const { id } = useParams(); // Получаем ID матча из URL
  const [match, setMatch] = useState(null);

  useEffect(() => {

    fetch(`http://127.0.0.1:8000/api/nhl/match/${id}`) // Загружаем данные о матче
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
            <h1>{match.match_info.home_team}</h1>
            <table className="stat-info">
              <colgroup>
                <col style={{ width: '150px' }} />
              </colgroup>
              <thead>
                <tr>
                  <th>Нападающий</th>
                  <th>G</th>
                  <th>A</th>
                  <th>+/-</th>
                  <th>S</th>
                  <th>SM</th>
                  <th>BS</th>
                  <th>PN</th>
                  <th>PIM</th>
                  <th>HT</th>
                  <th>TK</th>
                  <th>GV</th>
                </tr>
              </thead>
              {match.match_info.home_forward_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.g}</td>
                  <td>{p.a}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.s}</td>
                  <td>{p.sm}</td>
                  <td>{p.bs}</td>
                  <td>{p.pn}</td>
                  <td>{p.pim}</td>
                  <td>{p.ht}</td>
                  <td>{p.tk}</td>
                  <td>{p.gv}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Защитник</th>
                  <th>G</th>
                  <th>A</th>
                  <th>+/-</th>
                  <th>S</th>
                  <th>SM</th>
                  <th>BS</th>
                  <th>PN</th>
                  <th>PIM</th>
                  <th>HT</th>
                  <th>TK</th>
                  <th>GV</th>
                </tr>
              </thead>
              {match.match_info.home_defenseman_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.g}</td>
                  <td>{p.a}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.s}</td>
                  <td>{p.sm}</td>
                  <td>{p.bs}</td>
                  <td>{p.pn}</td>
                  <td>{p.pim}</td>
                  <td>{p.ht}</td>
                  <td>{p.tk}</td>
                  <td>{p.gv}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Вратарь</th>
                  <th>SA</th>
                  <th>GA</th>
                  <th>SV</th>
                  <th>SV %</th>
                  <th>ESSV</th>
                  <th>PPSV</th>
                </tr>
              </thead>
              {match.match_info.home_goalie_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.sa}</td>
                  <td>{p.ga}</td>
                  <td>{p.sv}</td>
                  <td>{p.sv_procent}</td>
                  <td>{p.essv}</td>
                  <td>{p.ppsv}</td>
                </tbody>
              ))}
            </table>

           
          </div>

          {/* Блок 2 - Инфа о второй команде */}
          <div className="block-info">
            <h1>{match.match_info.away_team}</h1>
            <table className="stat-info">
              <colgroup>
                <col style={{ width: '150px' }} />
              </colgroup>
              <thead>
                <tr>
                  <th>Нападающий</th>
                  <th>G</th>
                  <th>A</th>
                  <th>+/-</th>
                  <th>S</th>
                  <th>SM</th>
                  <th>BS</th>
                  <th>PN</th>
                  <th>PIM</th>
                  <th>HT</th>
                  <th>TK</th>
                  <th>GV</th>
                </tr>
              </thead>
              {match.match_info.away_forward_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.g}</td>
                  <td>{p.a}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.s}</td>
                  <td>{p.sm}</td>
                  <td>{p.bs}</td>
                  <td>{p.pn}</td>
                  <td>{p.pim}</td>
                  <td>{p.ht}</td>
                  <td>{p.tk}</td>
                  <td>{p.gv}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Защитник</th>
                  <th>G</th>
                  <th>A</th>
                  <th>+/-</th>
                  <th>S</th>
                  <th>SM</th>
                  <th>BS</th>
                  <th>PN</th>
                  <th>PIM</th>
                  <th>HT</th>
                  <th>TK</th>
                  <th>GV</th>
                </tr>
              </thead>
              {match.match_info.away_defenseman_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.g}</td>
                  <td>{p.a}</td>
                  <td>{p.plus_minus}</td>
                  <td>{p.s}</td>
                  <td>{p.sm}</td>
                  <td>{p.bs}</td>
                  <td>{p.pn}</td>
                  <td>{p.pim}</td>
                  <td>{p.ht}</td>
                  <td>{p.tk}</td>
                  <td>{p.gv}</td>
                </tbody>
              ))}
              <thead>
                <tr>
                  <th>Вратарь</th>
                  <th>SA</th>
                  <th>GA</th>
                  <th>SV</th>
                  <th>SV %</th>
                  <th>ESSV</th>
                  <th>PPSV</th>
                </tr>
              </thead>
              {match.match_info.away_goalie_players.map((p, index) => (
                <tbody>
                  <td>{p.player}</td>
                  <td>{p.sa}</td>
                  <td>{p.ga}</td>
                  <td>{p.sv}</td>
                  <td>{p.sv_procent}</td>
                  <td>{p.essv}</td>
                  <td>{p.ppsv}</td>
                </tbody>
              ))}
            </table>
          </div>
      </main>
    </div>
  );
}

export default MatchDetailNHL;
