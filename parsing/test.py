import psycopg2
import configparser

try:
    # Загружаем конфиг
    config = configparser.ConfigParser()
    config.read("config.ini")
    db_params = config["postgresql"]

    # Подключаемся к БД
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Название таблицы, которую хотим проверить
    table_name = "nba_bet"  # Измените на нужную вам таблицу

    # Запрос списка колонок

    cur.execute(f"SELECT 'match_ID' FROM nba_match;")
    inf = cur.fetchall()

    if len(inf) != 0:
        print(False)
    else:
        print(True)

    # Закрываем соединение
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("❌ Ошибка при получении списка полей!")
    print(str(e))
