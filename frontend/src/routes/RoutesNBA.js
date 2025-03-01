import { Routes, Route } from "react-router-dom";
import MatchDetailNBA from "../pages/NBA/MatchDetailNBA";
import TotalDetailNBA from "../pages/NBA/TotalDetailNBA";
import MoneylineDetailNBA from "../pages/NBA/MoneylineDetailNBA";
import HandicapDetailNBA from "../pages/NBA/HandicapDetailNBA";

const RoutesNBA = () => {
  return (
    <Routes>
      <Route path="match/:id" element={<MatchDetailNBA />} />
      <Route path="match/:id/total" element={<TotalDetailNBA />} />
      <Route path="match/:id/moneyline" element={<MoneylineDetailNBA />} />
      <Route path="match/:id/handicap" element={<HandicapDetailNBA />} />
    </Routes>
  );
};

export default RoutesNBA;
