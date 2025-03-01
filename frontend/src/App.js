import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RoutesNBA from "./routes/RoutesNBA"; // Импортируем роуты NBA
import MatchDetailNFL from "./pages/MatchDetailNFL";

function App() {
  console.log("Router работает");

  return (
    <Routes>
      <Route path="/" element={<Home />} /> {/* Главная страница */}
      
      {/* Родительский маршрут NBA */}
      <Route path="/nba/*" element={<RoutesNBA />} />

      {/* NFL матч */}
      <Route path="/nfl/match/:id" element={<MatchDetailNFL />} />
    </Routes>
  );
}

export default App;
