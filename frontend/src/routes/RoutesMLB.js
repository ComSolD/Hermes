import { Routes, Route } from "react-router-dom";
import MatchDetailMLB from "../pages/MLB/MatchDetailMLB";
import TotalDetailMLB from "../pages/MLB/TotalDetailMLB";
import MoneylineDetailMLB from "../pages/MLB/MoneylineDetailMLB";
import HandicapDetailMLB from "../pages/MLB/HandicapDetailMLB";
import ScheduleMLB from "../pages/MLB/ScheduleMLB";
// import TeamsMLB from "../pages/MLB/TeamsMLB";
import StatisticMLB from "../pages/MLB/StatisticMLB";

const RoutesMLB = () => {
  return (
    <Routes>
      <Route path="match/:id" element={<MatchDetailMLB />} />
      <Route path="match/:id/total/:period" element={<TotalDetailMLB />} />
      <Route path="match/:id/moneyline" element={<MoneylineDetailMLB />} />
      <Route path="match/:id/handicap/:period" element={<HandicapDetailMLB />} />
      <Route path="schedule/:date?" element={<ScheduleMLB />} />
      {/* <Route path="teams" element={<TeamsMLB />} /> */}
      <Route path="statistic" element={<StatisticMLB />} />
    </Routes>
  );
};

export default RoutesMLB;
