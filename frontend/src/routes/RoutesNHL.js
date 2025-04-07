import { Routes, Route } from "react-router-dom";
import MatchDetailNHL from "../pages/NHL/MatchDetailNHL";
import TotalDetailNHL from "../pages/NHL/TotalDetailNHL";
import MoneylineDetailNHL from "../pages/NHL/MoneylineDetailNHL";
import XBetDetailNHL from "../pages/NHL/XBetDetailNHL";
import HandicapDetailNHL from "../pages/NHL/HandicapDetailNHL";
import ScheduleNHL from "../pages/NHL/ScheduleNHL";
// import TeamsNHL from "../pages/NHL/TeamsNHL";
import StatisticNHL from "../pages/NHL/StatisticNHL";
import StandingsNHL from "../pages/NHL/StandingsNHL";

const RoutesNHL = () => {
  return (
    <Routes>
      <Route path="match/:id" element={<MatchDetailNHL />} />
      <Route path="match/:id/total/:period" element={<TotalDetailNHL />} />
      <Route path="match/:id/moneyline" element={<MoneylineDetailNHL />} />
      <Route path="match/:id/1x2" element={<XBetDetailNHL />} />
      <Route path="match/:id/handicap/:period" element={<HandicapDetailNHL />} />
      <Route path="schedule/:date?" element={<ScheduleNHL />} />
      {/* <Route path="teams" element={<TeamsNHL />} /> */}
      <Route path="statistic" element={<StatisticNHL />} />
      <Route path="standings" element={<StandingsNHL />} />
    </Routes>
  );
};

export default RoutesNHL;
