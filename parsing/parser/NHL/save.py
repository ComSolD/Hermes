from datetime import datetime
import psycopg2
import configparser
import uuid


def team_table(name_team1, name_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(f"SELECT team_id FROM nhl_team WHERE name = '{name_team1}';")

    team1_id = cur.fetchall()

    if len(team1_id) == 0:
        team1_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nhl_team(team_id, name) VALUES('{team1_id}', '{name_team1}')")
        conn.commit()
    else:
        team1_id = team1_id[0][0]


    cur.execute(f"SELECT team_id FROM nhl_team WHERE name = '{name_team2}';")

    team2_id = cur.fetchall()

    if len(team2_id) == 0:
        team2_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nhl_team(team_id, name) VALUES('{team2_id}', '{name_team2}')")
        conn.commit()
    else:
        team2_id = team2_id[0][0]

    return team1_id, team2_id


def bet_predict_tables(match_id, teams_id, bet_predict):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    bet_id = str(uuid.uuid4())

    cur.execute(f"INSERT INTO nhl_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_id}', '{match_id}', '{teams_id[0]}', '{teams_id[1]}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})")
    conn.commit()


def bet_result_tables(match_id, teams, result_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nhl_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nhl_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nhl_bet WHERE match_id = '{match_id}';")
        spread = cur.fetchall()[0][0]

        if spread < 0:
            spread_result = int(match_total[0]) - int(match_total[1]) + spread

            if spread_result > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_result = int(match_total[1]) - int(match_total[0]) - spread

            if spread_result > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]


        cur.execute(f'''UPDATE nhl_bet SET ml_result = '{teams[0] if result_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
        conn.commit()

    else:

        bet_id = str(uuid.uuid4())

        spread = float(bet[5])

        if '-' in bet[5]:
            spread_result = int(match_total[0]) - int(match_total[1]) + spread

            if spread_result > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_result = int(match_total[1]) - int(match_total[0]) - spread

            if spread_result > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]
            

        cur.execute(f'''INSERT INTO nhl_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, ml_result, total, over_total_parlay, under_total_parlay, total_result, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay, spread_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', {bet[0]}, {bet[1]},'{teams[0] if result_team1 == "Win" else teams[1]}', {bet[2]}, {bet[3]}, {bet[4]}, '{'over' if float(bet[2]) < (int(match_total[0]) + int(match_total[1])) else 'under'}', {bet[5]}, {bet[6]}, {bet[7]}, {bet[8]}, '{spread_team}');''')
        conn.commit()


def bet_old_result_tables(match_id, teams, result_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nhl_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nhl_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nhl_bet WHERE match_id = '{match_id}';")
        spread = cur.fetchall()[0][0]

        if spread < 0:
            spread_result = int(match_total[0]) - int(match_total[1]) + spread

            if spread_result > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_result = int(match_total[1]) - int(match_total[0]) + spread

            if spread_result > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]


        cur.execute(f'''UPDATE nhl_bet SET ml_result = '{teams[0] if result_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
        conn.commit()

    else:

        bet_id = str(uuid.uuid4())

        bet_id = str(uuid.uuid4())

        cur.execute(f'''INSERT INTO nhl_bet(bet_id, match_id, team1_id, team2_id, {"ml_team1_parlay" if bet[0] == 'Team1' else "ml_team2_parlay"}, ml_result, total, total_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', {bet[1]}, '{teams[0] if result_team1 == "Win" else teams[1]}', {bet[2]}, '{'over' if bet[2] < (int(match_total[0]) + int(match_total[1])) else 'under'}');''')
        conn.commit()


def match_table(match_id, teams, status, season, stage, date_match):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    if status == 'None':

        cur.execute("SELECT 1 FROM nhl_match WHERE match_id = %s AND status = 'null';", (match_id,))
        exists = cur.fetchone()


        if not exists:
            cur.execute(f"INSERT INTO nhl_match(match_id, team1_id, team2_id, season, stage, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{season}', '{stage}', '{date_match}')")
            conn.commit()

            return True

    else:
        
        cur.execute("SELECT 1 FROM nhl_match WHERE match_id = %s AND status = 'null';", (match_id,))
        exists = cur.fetchone()

        cur.execute("SELECT 1 FROM nhl_match WHERE match_id = %s;", (match_id,))
        just_match = cur.fetchone()


        if exists:
            cur.execute(f'''UPDATE nhl_match SET status = '{status}' WHERE match_id = '{match_id}';''')
            conn.commit()

            return True

        elif not just_match:
            cur.execute(f"INSERT INTO nhl_match(match_id, team1_id, team2_id, status, season, stage, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{status}', '{season}', '{stage}', '{date_match}')")
            conn.commit()

            return True


def team_stat_tables(match_id, teams_id, result_team1, result_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Заполнение таблицы статистики команд
    team1_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nhl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team1_Stat_id}', '{match_id}', '{teams_id[0]}', '{result_team1}', 'Away')")
    conn.commit()

    team2_Stat_id = str(uuid.uuid4()) 
    cur.execute(f"INSERT INTO nhl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team2_Stat_id}', '{match_id}', '{teams_id[1]}', '{result_team2}', 'Home')")
    conn.commit()


def team_stat_pts_tables(match_id, teams_id, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Заполнение таблицы статистики очков команд
    team1_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nhl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_t1, total_t1_missed, total_t2, total_t2_missed, total_t3, total_t3_missed) VALUES('{team1_PTS_Stat_id}', '{match_id}', '{teams_id[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]})")
    conn.commit()

    team2_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nhl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_t1, total_t1_missed, total_t2, total_t2_missed, total_t3, total_t3_missed) VALUES('{team2_PTS_Stat_id}', '{match_id}', '{teams_id[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]})")
    conn.commit()


def player_tables(match_id, team_id, forwards_team, defensemen_team, goalies_team):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    for player_name in forwards_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM nhl_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO nhl_player(player_id, name) VALUES(%s, %s)''', (player_id,player_name[-2]))
            conn.commit()


        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id , team_id, position, g, a, plus_minus, s, sm, bs, pn, pim, ht, tk, gv) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Forward', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]})''')
        conn.commit()

    

    # Заполнение таблицы игроков скамейки
    for player_name in defensemen_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM nhl_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO nhl_player(player_id, name) VALUES(%s, %s)''', (player_id,player_name[-2]))
            conn.commit()

        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id, team_id, position, g, a, plus_minus, s, sm, bs, pn, pim, ht, tk, gv) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Defense', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]})''')
        conn.commit()


    for player_name in goalies_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM nhl_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO nhl_player(player_id, name) VALUES(%s, %s)''', (player_id,player_name[-2]))
            conn.commit()

        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id, team_id, position, sa, ga, sv, sv_procent, essv, ppsv, pim) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Goaltender', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
        conn.commit()


def update_time():
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

     # SQL-запрос для обновления времени
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    # Проверяем, есть ли запись в таблице NHLUpdate
    cur.execute("SELECT id FROM nhl_update ORDER BY id DESC LIMIT 1;")
    last_record = cur.fetchone()

    if last_record:
        # Если запись есть – обновляем `updated_at`
        cur.execute("UPDATE nhl_update SET updated_at = %s WHERE id = %s;", (now, last_record[0]))
    else:
        # Если записей нет – создаём первую запись
        cur.execute("INSERT INTO nhl_update (updated_at) VALUES (%s);", (now,))

    # Фиксируем изменения и закрываем соединение
    conn.commit()

    cur.close()
    conn.close()

