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

    cur.execute(f"SELECT team_id FROM nfl_team WHERE name = '{name_team1}';")

    team1_id = cur.fetchall()

    if len(team1_id) == 0:
        team1_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nfl_team(team_id, name) VALUES('{team1_id}', '{name_team1}')")
        conn.commit()
    else:
        team1_id = team1_id[0][0]


    cur.execute(f"SELECT team_id FROM nfl_team WHERE name = '{name_team2}';")

    team2_id = cur.fetchall()

    if len(team2_id) == 0:
        team2_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nfl_team(team_id, name) VALUES('{team2_id}', '{name_team2}')")
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

    cur.execute(f"INSERT INTO nfl_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_id}', '{match_id}', '{teams_id[0]}', '{teams_id[1]}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})")
    conn.commit()


def bet_result_tables(match_id, teams, result_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nfl_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nfl_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nfl_bet WHERE match_id = '{match_id}';")
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


        cur.execute(f'''UPDATE nfl_bet SET ml_result = '{teams[0] if result_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
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
            

        cur.execute(f'''INSERT INTO nfl_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, ml_result, total, over_total_parlay, under_total_parlay, total_result, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay, spread_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', {bet[0]}, {bet[1]},'{teams[0] if result_team1 == "Win" else teams[1]}', {bet[2]}, {bet[3]}, {bet[4]}, '{'over' if float(bet[2]) < (int(match_total[0]) + int(match_total[1])) else 'under'}', {bet[5]}, {bet[6]}, {bet[7]}, {bet[8]}, '{spread_team}');''')
        conn.commit()


def bet_old_result_tables(match_id, teams, result_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nfl_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nfl_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nfl_bet WHERE match_id = '{match_id}';")
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


        cur.execute(f'''UPDATE nfl_bet SET ml_result = '{teams[0] if result_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
        conn.commit()

    else:

        bet_id = str(uuid.uuid4())

        if bet[0] == "Team1":
            spread_result = int(match_total[0]) - int(match_total[1]) + bet[1]

            team1_spread = bet[1]
            team2_spread = abs(bet[1])

            if spread_result > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]

        else:
            spread_result = int(match_total[1]) - int(match_total[0]) + bet[1]

            team2_spread = bet[1]
            team1_spread = abs(bet[1])

            if spread_result > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]

            
        cur.execute(f'''INSERT INTO nfl_bet(bet_id, match_id, team1_id, team2_id, ml_result, total, total_result, spread_team1, spread_team2, spread_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', '{teams[0] if result_team1 == "Win" else teams[1]}', {bet[2]}, '{'over' if bet[2] < (int(match_total[0]) + int(match_total[1])) else 'under'}', '{team1_spread}', '{team2_spread}', '{spread_team}');''')
        conn.commit()


def match_table(match_id, teams_id, season, game_stage, week_match, season_type):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM nfl_match WHERE match_id = %s", (match_id,))
    exists = cur.fetchone()


    if not exists:
        cur.execute(f"INSERT INTO nfl_match(match_id, team1_id, team2_id, season, stage, week, season_type) VALUES('{match_id}', '{teams_id[0]}', '{teams_id[1]}', '{season}', '{game_stage}', '{week_match}', '{season_type}')")
        conn.commit()

        return True


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
    cur.execute(f"INSERT INTO nfl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_q1, total_q1_missed, total_q2, total_q2_missed, total_q3, total_q3_missed, total_q4, total_q4_missed) VALUES('{team1_PTS_Stat_id}', '{match_id}', '{teams_id[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]}, {total[0][6]}, {total[0][7]})")
    conn.commit()

    team2_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nfl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_q1, total_q1_missed, total_q2, total_q2_missed, total_q3, total_q3_missed, total_q4, total_q4_missed) VALUES('{team2_PTS_Stat_id}', '{match_id}', '{teams_id[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]}, {total[1][6]}, {total[1][7]})")
    conn.commit()


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
    cur.execute(f"INSERT INTO nfl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team1_Stat_id}', '{match_id}', '{teams_id[0]}', '{result_team1}', 'Away')")
    conn.commit()

    team2_Stat_id = str(uuid.uuid4()) 
    cur.execute(f"INSERT INTO nfl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team2_Stat_id}', '{match_id}', '{teams_id[1]}', '{result_team2}', 'Home')")
    conn.commit()


def player_tables(match_id, team_id, team_passing, team_rushing, team_receiving, team_fumbles, team_defense, team_interceptions, team_kick_returns, team_punt_returns, team_kicking, team_punting):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    if team_passing:
        for player_name in team_passing:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()


            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, c, att, yds, avg, td, interception,  sack, trying_sack, qbr, rtg) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Passing', {player_name[2][0]}, {player_name[2][1]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7][0]}, {player_name[7][1]}, {'null' if player_name[8] == '--' else player_name[8]}, {player_name[9]})''')
            conn.commit()

    
    if team_rushing:
        for player_name in team_rushing:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, car, yds, avg, td, long) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Rushing', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()

    
    if team_receiving:
        for player_name in team_receiving:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, rec, yds, avg, td, long, tgts) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Receiving', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]})''')
            conn.commit()

    
    if team_fumbles:
        for player_name in team_fumbles:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, fum, lost, rec) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Fumbles', {player_name[2]}, {player_name[3]}, {player_name[4]})''')
            conn.commit()

    
    if team_defense:
        for player_name in team_defense:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, tot, solo, sacks, tfl, pd, qb_hts, td) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Defense', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]})''')
            conn.commit()

    
    if team_interceptions:
        for player_name in team_interceptions:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, interception, yds, td) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Interceptions', {player_name[2]}, {player_name[3]}, {player_name[4]})''')
            conn.commit()

    
    if team_kick_returns:
        for player_name in team_kick_returns:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, no, yds, avg, long, td) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Kick Returns', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()
    

    if team_punt_returns:
        for player_name in team_punt_returns:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, no, yds, avg, long, td) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Punt Returns', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()

    
    if team_kicking:
        for player_name in team_kicking:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, fg, trying_fg, pct, long, xp, trying_xp, pts) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Kicking', {player_name[2][0]}, {player_name[2][1]}, {player_name[3]}, {player_name[4]}, {player_name[5][0]}, {player_name[5][1]}, {player_name[6]})''')
            conn.commit()


    if team_punting:
        for player_name in team_punting:

            player_name = player_name[:2] + player_name[2]

            player_id = player_name[1]

            cur.execute(f'''SELECT player_id FROM nfl_player WHERE player_id = '{player_id}';''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute('''INSERT INTO nfl_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[0]))
                conn.commit()

            stat_id = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO nfl_player_stat(stat_id, player_id, match_id, team_id, position, no, yds, avg, tb, in_20, long) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Punting', {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]})''')
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

    # Проверяем, есть ли запись в таблице NFLUpdate
    cur.execute("SELECT id FROM nfl_update ORDER BY id DESC LIMIT 1;")
    last_record = cur.fetchone()

    if last_record:
        # Если запись есть – обновляем `updated_at`
        cur.execute("UPDATE nfl_update SET updated_at = %s WHERE id = %s;", (now, last_record[0]))
    else:
        # Если записей нет – создаём первую запись
        cur.execute("INSERT INTO nfl_update (updated_at) VALUES (%s);", (now,))

    # Фиксируем изменения и закрываем соединение
    conn.commit()

    cur.close()
    conn.close()

