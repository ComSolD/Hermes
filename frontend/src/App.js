import { Routes, Route } from "react-router-dom";
import Home from "./Home";
import MatchDetailNBA from "./MatchDetailNBA"; // ✅ Импортируем страницу матча
import MatchDetailNFL from "./MatchDetailNFL"; // ✅ Импортируем страницу матча

function App() {
  console.log("Router работает");
  
  return (
    <Routes> 
        <Route path="/" element={<Home />} />  {/* Главная страница */}
        <Route path="/nba/match/:id" element={<MatchDetailNBA />} /> {/* ✅ Новый маршрут */}
        <Route path="/nfl/match/:id" element={<MatchDetailNFL />} /> {/* ✅ Новый маршрут */}
    </Routes>
  );
}

export default App;
