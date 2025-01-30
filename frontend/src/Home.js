import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Home.css";

function Home() {
  const [message, setMessage] = useState(""); // Хранение сообщения
  const [loading, setLoading] = useState(true); // Индикатор загрузки

  useEffect(() => {
    document.title = "Главная страница";
    // Загрузка данных с сервера
    axios.get("http://127.0.0.1:8000/") // Укажите ваш URL
      .then((response) => {
        if (response.data.message) {
          setMessage(response.data.message); // Сохраняем текст первого сообщения
        } else {
          setMessage("Сообщение отсутствует");
        }
        setLoading(false); // Завершаем загрузку
      })
      .catch((error) => {
        console.error("Ошибка при загрузке данных:", error);
        setMessage("Ошибка при загрузке данных");
        setLoading(false); // Завершаем загрузку
      });
  }, []);

  return (
    <div>
      <header>
        {/* Логотип */}
        <div className="logo">
          <img
            src="/image.png"
            alt="React Logo"
            style={{ width: "40px", marginRight: "10px" }}
          />
          InsightFlow
        </div>

        {/* Навигация */}
        <nav>
          <a href="#nba">NBA</a>
          <a href="#nfl">NFL</a>
          <a href="#nhl">NHL</a>
          <a href="#mlb">MLB</a>
        </nav>
      </header>
      <main>
        {loading ? (
          <h1>Загрузка...</h1>
        ) : (
          <h1>{message}</h1>
        )}
      </main>
    </div>
  );
}

export default Home;
