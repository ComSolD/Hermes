import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import MatchDetailNBA from "./pages/NBA/MatchDetailNBA"; // ✅ Импортируем страницу матча
import TotalDetailNBA from "./pages/NBA/TotalDetailNBA"; // ✅ Импортируем страницу матча
import MatchDetailNFL from "./pages/MatchDetailNFL"; // ✅ Импортируем страницу матча

function App() {
  console.log("Router работает");
  
  return (
    <Routes> 
        <Route path="/" element={<Home />} />  {/* Главная страница */}
        <Route path="/nba/match/:id" element={<MatchDetailNBA />} /> {/* ✅ Новый маршрут */}
        <Route path="/nba/match/:id/total" element={<TotalDetailNBA />} /> {/* ✅ Новый маршрут */}

        
        <Route path="/nfl/match/:id" element={<MatchDetailNFL />} /> {/* ✅ Новый маршрут */}
    </Routes>
  );
}

export default App;
