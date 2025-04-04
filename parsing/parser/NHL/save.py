from datetime import datetime
import psycopg2
import configparser

import uuid

from dictionary.NHL import getDictionary


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


def match_table(match_id, teams, season, date_match, stage, status, time):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM nhl_match WHERE match_id = %s", (match_id,))
    exists = cur.fetchone()

    cur.execute("SELECT stage FROM nhl_match WHERE match_id = %s", (match_id,))
    stage_check = cur.fetchone()
        

    if not exists and season != '':

        cur.execute(f"INSERT INTO nhl_match(match_id, team1_id, team2_id, season, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{season}', '{date_match}')")
        conn.commit()

        return False
    
    elif exists and stage_check[0] is None and stage != '':
        cur.execute(f'''UPDATE nhl_match SET stage = '{stage}', status = '{status}', time = '{time}' WHERE match_id = '{match_id}';''')
        conn.commit()

        return False
    

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
    cur.execute(f"INSERT INTO nhl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team1_Stat_id}', '{match_id}', '{teams_id[0]}', '{result_team1}', 'away')")
    conn.commit()

    team2_Stat_id = str(uuid.uuid4()) 
    cur.execute(f"INSERT INTO nhl_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team2_Stat_id}', '{match_id}', '{teams_id[1]}', '{result_team2}', 'home')")
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
    cur.execute(f"INSERT INTO nhl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_p1, total_p1_missed, total_p2, total_p2_missed, total_p3, total_p3_missed) VALUES('{team1_PTS_Stat_id}', '{match_id}', '{teams_id[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]})")
    conn.commit()

    team2_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nhl_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_p1, total_p1_missed, total_p2, total_p2_missed, total_p3, total_p3_missed) VALUES('{team2_PTS_Stat_id}', '{match_id}', '{teams_id[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]})")
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

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id , team_id, position, g, a, plus_minus, s, sm, bs, pn, pim, ht, tk, gv) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'forward', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]})''')
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

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id, team_id, position, g, a, plus_minus, s, sm, bs, pn, pim, ht, tk, gv) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'defenseman', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]})''')
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

        cur.execute(f'''INSERT INTO nhl_player_stat(stat_id, player_id, match_id, team_id, position, sa, ga, sv, sv_procent, essv, ppsv, pim) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'goalie', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
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


def odds_moneyline_table(match_id, team1_moneyline, team2_moneyline, period):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    bet_id = str(uuid.uuid4())

    cur.execute(f"INSERT INTO nhl_moneyline_bet(moneyline_bet_id, match_id, team1_odds, team2_odds, period) VALUES('{bet_id}', '{match_id}', '{team1_moneyline}', '{team2_moneyline}', '{period}')")
    conn.commit()


def moneyline_result_table(match_id, teams_ID, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period FROM nhl_moneyline_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if value[0] > value[1]:
            result = teams_ID[0]
        elif value[0] < value[1]:
            result = teams_ID[1]
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nhl_moneyline_bet SET result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}';''')
        conn.commit()


def odds_total_table(match_id, odds, period):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    for odd in odds:
        bet_id = str(uuid.uuid4())

        try:
            cur.execute(f"INSERT INTO nhl_total_bet(total_bet_id, match_id, total, over_odds, under_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[1]}, {odd[2]}, '{period}')")
            conn.commit()
        except:
            pass


def total_result_table(match_id, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period, total FROM nhl_total_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if period[1] > value[0] + value[1]:
            result = 'under'
        elif period[1] < value[0] + value[1]:
            result = 'over'
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nhl_total_bet SET total_result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND total = {period[1]};''')
        conn.commit()


def odds_handicap_table(match_id, odds, period):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    for odd in odds:
        bet_id = str(uuid.uuid4())

        cur.execute(f"INSERT INTO nhl_handicap_bet(handicap_bet_id, match_id, handicap, handicap_team1_odds, handicap_team2_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[2]}, {odd[1]}, '{period}')")
        conn.commit()


def handicap_result_table(match_id, teams_ID, handicap):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period, handicap FROM nhl_handicap_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], handicap)

        if period[1] > 0:
            handi = -period[1]
        elif period[1] < 0:
            handi = abs(period[1])
        else:
            handi = period[1]


        if 0 < value[0] - value[1] + handi:
            team1_result = 'win'
        elif 0 == value[0] - value[1] + handi:
            team1_result = 'draw'
        else:
            team1_result = 'lose'

        if 0 < value[1] - value[0] + period[1]:
            team2_result = 'win'
        elif 0 == value[1] - value[0] + period[1]:
            team2_result = 'draw'
        else:
            team2_result = 'lose'

        cur.execute(f'''UPDATE nhl_handicap_bet SET handicap_team1_result = '{team1_result}', handicap_team2_result = '{team2_result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND handicap = {period[1]};''')
        conn.commit()


def odds_x_table(match_id, team1_moneyline, draw, team2_moneyline, period):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    bet_id = str(uuid.uuid4())

    cur.execute(f"INSERT INTO nhl_x_bet(x_bet_id, match_id, team1_odds, draw, team2_odds, period) VALUES('{bet_id}', '{match_id}', {team1_moneyline}, {draw}, {team2_moneyline}, '{period}')")
    conn.commit()


def x_result_table(match_id, teams_ID, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period FROM nhl_x_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if value[0] > value[1]:
            result = teams_ID[0]
        elif value[0] < value[1]:
            result = teams_ID[1]
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nhl_x_bet SET result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}';''')
        conn.commit()

