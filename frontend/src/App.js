import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RoutesNBA from "./routes/RoutesNBA"; // Импортируем роуты NBA
import RoutesMLB from "./routes/RoutesMLB"; // Импортируем роуты MLB

import MatchDetailNFL from "./pages/MatchDetailNFL";

function App() {
  console.log("Router работает");

  return (
    <Routes>
      <Route path="/" element={<Home />} /> {/* Главная страница */}
      
      {/* Родительский маршрут NBA */}
      <Route path="/nba/*" element={<RoutesNBA />} />

      {/* Родительский маршрут MLB */}
      <Route path="/mlb/*" element={<RoutesMLB />} />

      {/* NFL матч */}
      <Route path="/nfl/match/:id" element={<MatchDetailNFL />} />
    </Routes>
  );
}

export default App;
