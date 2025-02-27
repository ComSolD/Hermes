from datetime import datetime
import psycopg2
import configparser

import uuid

from dictionary.NBA import getDictionary


def team_table(name_team1, name_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(f"SELECT team_id FROM nba_team WHERE name = '{name_team1}';")

    team1_id = cur.fetchall()

    if len(team1_id) == 0:
        team1_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nba_team(team_id, name) VALUES('{team1_id}', '{name_team1}')")
        conn.commit()
    else:
        team1_id = team1_id[0][0]


    cur.execute(f"SELECT team_id FROM nba_team WHERE name = '{name_team2}';")

    team2_id = cur.fetchall()

    if len(team2_id) == 0:
        team2_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO nba_team(team_id, name) VALUES('{team2_id}', '{name_team2}')")
        conn.commit()
    else:
        team2_id = team2_id[0][0]

    return team1_id, team2_id


def team_table_espn(name_team1, name_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(f"SELECT team_id, name FROM nba_team WHERE name = '{name_team1}' OR second_name = '{name_team1}';")

    team1_id = cur.fetchall()

    team1_name = team1_id[0][1]

    team1_id = team1_id[0][0]

    cur.execute(f"SELECT team_id, name FROM nba_team WHERE name = '{name_team2}' OR second_name = '{name_team2}';")

    team2_id = cur.fetchall()

    team2_name = team2_id[0][1]

    team2_id = team2_id[0][0]
    

    return team1_id, team2_id, team1_name, team2_name


def team_stat_tables(match_id, teams_id, resul_team1, resul_team2, stat_team1, stat_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Заполнение таблицы статистики команд
    team1_Stat_id = str(uuid.uuid4())
    cur.execute(f'''INSERT INTO nba_team_stat(team_stat_id, match_id, team_id, result, status, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf) VALUES('{team1_Stat_id}', '{match_id}', '{teams_id[0]}', '{resul_team1}', 'Away', {stat_team1[0][0]}, {stat_team1[0][1]}, {stat_team1[1][0]}, {stat_team1[1][1]}, {stat_team1[2][0]}, {stat_team1[2][1]}, {int(stat_team1[3])}, {int(stat_team1[4])}, {int(stat_team1[5])}, {int(stat_team1[6])}, {int(stat_team1[7])}, {int(stat_team1[8])}, {int(stat_team1[9])}, {int(stat_team1[10])})''')
    conn.commit()

    team2_Stat_id = str(uuid.uuid4()) 
    cur.execute(f'''INSERT INTO nba_team_stat(team_stat_id, match_id, team_id, result, status, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf) VALUES('{team2_Stat_id}', '{match_id}', '{teams_id[1]}', '{resul_team2}', 'Home', {stat_team2[0][0]}, {stat_team2[0][1]}, {stat_team2[1][0]}, {stat_team2[1][1]}, {stat_team2[2][0]}, {stat_team2[2][1]}, {int(stat_team2[3])}, {int(stat_team2[4])}, {int(stat_team2[5])}, {int(stat_team2[6])}, {int(stat_team2[7])}, {int(stat_team2[8])}, {int(stat_team2[9])}, {int(stat_team2[10])})''')
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
    cur.execute(f"INSERT INTO nba_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_q1, total_q1_missed, total_q2, total_q2_missed, total_q3, total_q3_missed, total_q4, total_q4_missed) VALUES('{team1_PTS_Stat_id}', '{match_id}', '{teams_id[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]}, {total[0][6]}, {total[0][7]})")
    conn.commit()

    team2_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO nba_team_pts_stat(team_pts_stat_id, match_id, team_id, total, total_missed, total_q1, total_q1_missed, total_q2, total_q2_missed, total_q3, total_q3_missed, total_q4, total_q4_missed) VALUES('{team2_PTS_Stat_id}', '{match_id}', '{teams_id[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]}, {total[1][6]}, {total[1][7]})")
    conn.commit()


def player_tables(match_id, team_id, starter_team, bench_team):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    for player_name in starter_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM nba_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO nba_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[-2]))
            conn.commit()


        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO nba_player_stat(stat_id, player_id, match_id ,team_id , position, pts, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf, plus_minus, min) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'starter', {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
        conn.commit()

    

    # Заполнение таблицы игроков скамейки
    for player_name in bench_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM nba_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO nba_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[-2]))
            conn.commit()

        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO nba_player_stat(stat_id, player_id, match_id ,team_id , position, pts, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf, plus_minus, min) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'bench', {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
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

    # Проверяем, есть ли запись в таблице NBAUpdate
    cur.execute("SELECT id FROM nba_update ORDER BY id DESC LIMIT 1;")
    last_record = cur.fetchone()

    if last_record:
        # Если запись есть – обновляем `updated_at`
        cur.execute("UPDATE nba_update SET updated_at = %s WHERE id = %s;", (now, last_record[0]))
    else:
        # Если записей нет – создаём первую запись
        cur.execute("INSERT INTO nba_update (updated_at) VALUES (%s);", (now,))

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

    cur.execute(f"INSERT INTO nba_moneyline_bet(moneyline_bet_id, match_id, team1_odds, team2_odds, period) VALUES('{bet_id}', '{match_id}', '{team1_moneyline}', '{team2_moneyline}', '{period}')")
    conn.commit()


def match_table(match_id, teams, season, date_match, stage):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM nba_match WHERE match_id = %s", (match_id,))
    exists = cur.fetchone()

    cur.execute("SELECT stage FROM nba_match WHERE match_id = %s", (match_id,))
    stage_check = cur.fetchone()
        

    if not exists and season != '':

        cur.execute(f"INSERT INTO nba_match(match_id, team1_id, team2_id, season, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{season}', '{date_match}')")
        conn.commit()

        return False
    
    elif exists and stage_check[0] is None and stage != '':

        cur.execute(f'''UPDATE nba_match SET stage = '{stage}' WHERE match_id = '{match_id}';''')
        conn.commit()

        return False
    

    return True


def moneyline_result_table(match_id, teams_ID, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period FROM nba_moneyline_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if value[0] > value[1]:
            result = teams_ID[0]
        elif value[0] < value[1]:
            result = teams_ID[1]
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nba_moneyline_bet SET result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}';''')
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
            cur.execute(f"INSERT INTO nba_total_bet(total_bet_id, match_id, total, over_odds, under_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[1]}, {odd[2]}, '{period}')")
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

    cur.execute("SELECT period, total FROM nba_total_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if period[1] > value[0] + value[1]:
            result = 'under'
        elif period[1] < value[0] + value[1]:
            result = 'over'
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nba_total_bet SET total_result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND total = {period[1]};''')
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

        cur.execute(f"INSERT INTO nba_handicap_bet(handicap_bet_id, match_id, handicap, handicap_team1_odds, handicap_team2_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[2]}, {odd[1]}, '{period}')")
        conn.commit()


def handicap_result_table(match_id, teams_ID, handicap):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period, handicap FROM nba_handicap_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], handicap)

        if 0 < value[0] - value[1] + period[1]:
            result = teams_ID[0]
        elif 0 < value[1] - value[0] + period[1]:
            result = teams_ID[1]
        else:
            result = 'draw'

        cur.execute(f'''UPDATE nba_handicap_bet SET handicap_result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND handicap = {period[1]};''')
        conn.commit()

