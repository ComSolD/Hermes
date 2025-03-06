import { Routes, Route } from "react-router-dom";
import MatchDetailNBA from "../pages/NBA/MatchDetailNBA";
import TotalDetailNBA from "../pages/NBA/TotalDetailNBA";
import MoneylineDetailNBA from "../pages/NBA/MoneylineDetailNBA";
import HandicapDetailNBA from "../pages/NBA/HandicapDetailNBA";
import ScheduleNBA from "../pages/NBA/ScheduleNBA";
import TeamsNBA from "../pages/NBA/TeamsNBA";
import StatisticNBA from "../pages/NBA/StatisticNBA";

const RoutesNBA = () => {
  return (
    <Routes>
      <Route path="match/:id" element={<MatchDetailNBA />} />
      <Route path="match/:id/total/:period" element={<TotalDetailNBA />} />
      <Route path="match/:id/moneyline" element={<MoneylineDetailNBA />} />
      <Route path="match/:id/handicap/:period" element={<HandicapDetailNBA />} />
      <Route path="schedule/:date?" element={<ScheduleNBA />} />
      <Route path="teams" element={<TeamsNBA />} />
      <Route path="statistic" element={<StatisticNBA />} />
    </Routes>
  );
};

export default RoutesNBA;
