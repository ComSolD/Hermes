import { Routes, Route } from "react-router-dom";
import Home from "./Home";
import MatchDetail from "./MatchDetail"; // ✅ Импортируем страницу матча

function App() {
  console.log("Router работает");
  
  return (
    <Routes> 
        <Route path="/" element={<Home />} />  {/* Главная страница */}
        <Route path="/match/:id" element={<MatchDetail />} /> {/* ✅ Новый маршрут */}
    </Routes>
  );
}

export default App;
