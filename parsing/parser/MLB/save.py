from datetime import datetime
import logging
import traceback
import psycopg2
import configparser

import uuid

from dictionary.MLB import getDictionary

def team_table(name_team1, name_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(f"SELECT team_id FROM mlb_team WHERE name = '{name_team1}';")

    team1_id = cur.fetchall()

    if len(team1_id) == 0:
        team1_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO mlb_team(team_id, name) VALUES('{team1_id}', '{name_team1}')")
        conn.commit()
    else:
        team1_id = team1_id[0][0]


    cur.execute(f"SELECT team_id FROM mlb_team WHERE name = '{name_team2}';")

    team2_id = cur.fetchall()

    if len(team2_id) == 0:
        team2_id = str(uuid.uuid4())
        cur.execute(f"INSERT INTO mlb_team(team_id, name) VALUES('{team2_id}', '{name_team2}')")
        conn.commit()
    else:
        team2_id = team2_id[0][0]

    return team1_id, team2_id


def match_table(match_id, teams, season, date_match, stage):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM mlb_match WHERE match_id = %s", (match_id,))
    exists = cur.fetchone()

    cur.execute("SELECT stage FROM mlb_match WHERE match_id = %s", (match_id,))
    stage_check = cur.fetchone()
        

    if not exists and stage == '':

        cur.execute(f"INSERT INTO mlb_match(match_id, team1_id, team2_id, season, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{season}', '{date_match}')")
        conn.commit()

        return False
    
    elif exists and stage_check[0] is None and stage != '':

        cur.execute(f'''UPDATE mlb_match SET stage = '{stage}' WHERE match_id = '{match_id}';''')
        conn.commit()

        return False
    

    return True


def team_stat_tables(match_id, teams_id, resul_team1, resul_team2):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Заполнение таблицы статистики команд
    team1_Stat_id = str(uuid.uuid4())
    cur.execute(f'''INSERT INTO mlb_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team1_Stat_id}', '{match_id}', '{teams_id[0]}', '{resul_team1}', 'away')''')
    conn.commit()

    team2_Stat_id = str(uuid.uuid4()) 
    cur.execute(f'''INSERT INTO mlb_team_stat(team_stat_id, match_id, team_id, result, status) VALUES('{team2_Stat_id}', '{match_id}', '{teams_id[1]}', '{resul_team2}', 'home')''')
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
    cur.execute(f"INSERT INTO mlb_team_pts_stat(team_pts_stat_id, match_id, team_id, run, run_missed, hit, hit_missed, error, run_i1, run_i1_missed, run_i2, run_i2_missed, run_i3, run_i3_missed, run_i4, run_i4_missed, run_i5, run_i5_missed, run_i6, run_i6_missed, run_i7, run_i7_missed, run_i8, run_i8_missed, run_i9, run_i9_missed) VALUES('{team1_PTS_Stat_id}', '{match_id}', '{teams_id[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][-4]}, {total[0][-3]}, {total[0][-5]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]}, {total[0][6]}, {total[0][7]}, {total[0][8]}, {total[0][9]}, {total[0][10]}, {total[0][11]}, {total[0][12]}, {total[0][13]}, {total[0][14]}, {total[0][15]}, {total[0][16]}, {total[0][17]})")
    conn.commit()

    team2_PTS_Stat_id = str(uuid.uuid4())
    cur.execute(f"INSERT INTO mlb_team_pts_stat(team_pts_stat_id, match_id, team_id, run, run_missed, hit, hit_missed, error, run_i1, run_i1_missed, run_i2, run_i2_missed, run_i3, run_i3_missed, run_i4, run_i4_missed, run_i5, run_i5_missed, run_i6, run_i6_missed, run_i7, run_i7_missed, run_i8, run_i8_missed, run_i9, run_i9_missed) VALUES('{team2_PTS_Stat_id}', '{match_id}', '{teams_id[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][-4]}, {total[1][-3]}, {total[1][-5]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]}, {total[1][6]}, {total[1][7]}, {total[1][8]}, {total[1][9]}, {total[1][10]}, {total[1][11]}, {total[1][12]}, {total[1][13]}, {total[1][14]}, {total[1][15]}, {total[1][16]}, {total[1][17]})")
    conn.commit()


def player_tables(match_id, team_id, pitcher_team, hitter_team):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    for player_name in pitcher_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM mlb_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO mlb_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[-2]))
            conn.commit()


        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO mlb_player_stat(stat_id, player_id, match_id ,team_id, position, role, ip, h, r, er, bb, k, hr, pc, st, era) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'pitcher', 'pitcher', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]})''')
        conn.commit()

    

    # Заполнение таблицы игроков скамейки
    for player_name in hitter_team:
        player_id = player_name[-1]

        cur.execute(f'''SELECT player_id FROM mlb_player WHERE player_id = '{player_id}';''')

        feed_back = cur.fetchall()

        if len(feed_back) == 0:
            cur.execute('''INSERT INTO mlb_player(player_id, name) VALUES(%s, %s)''', (player_id, player_name[-3]))
            conn.commit()

        stat_id = str(uuid.uuid4())

        if player_name[0] == '-':
            player_name[0] = 0

        cur.execute(f'''INSERT INTO mlb_player_stat(stat_id, player_id, match_id ,team_id , position, role, ab, r, h, rbi, hr, bb, k, avg, obp, slg) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'hitter', '{player_name[-2]}', {player_name[0]}, {player_name[1]}, {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]})''')
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
    cur.execute("SELECT id FROM mlb_update ORDER BY id DESC LIMIT 1;")
    last_record = cur.fetchone()

    if last_record:
        # Если запись есть – обновляем `updated_at`
        cur.execute("UPDATE mlb_update SET updated_at = %s WHERE id = %s;", (now, last_record[0]))
    else:
        # Если записей нет – создаём первую запись
        cur.execute("INSERT INTO mlb_update (updated_at) VALUES (%s);", (now,))

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

    cur.execute(f"INSERT INTO mlb_moneyline_bet(moneyline_bet_id, match_id, team1_odds, team2_odds, period) VALUES('{bet_id}', '{match_id}', '{team1_moneyline}', '{team2_moneyline}', '{period}')")
    conn.commit()


def moneyline_result_table(match_id, teams_ID, total):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period FROM mlb_moneyline_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if value[0] > value[1]:
            result = teams_ID[0]
        elif value[0] < value[1]:
            result = teams_ID[1]
        else:
            result = 'draw'

        cur.execute(f'''UPDATE mlb_moneyline_bet SET result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}';''')
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
            cur.execute(f"INSERT INTO mlb_total_bet(total_bet_id, match_id, total, over_odds, under_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[1]}, {odd[2]}, '{period}')")
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

    cur.execute("SELECT period, total FROM mlb_total_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], total)

        if period[1] > value[0] + value[1]:
            result = 'under'
        elif period[1] < value[0] + value[1]:
            result = 'over'
        else:
            result = 'draw'

        cur.execute(f'''UPDATE mlb_total_bet SET total_result = '{result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND total = {period[1]};''')
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

        try:
            cur.execute(f"INSERT INTO mlb_handicap_bet(handicap_bet_id, match_id, handicap, handicap_team1_odds, handicap_team2_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[2]}, {odd[1]}, '{period}')")
            conn.commit()
        except Exception as e:
            logging.error(f"Ошибка записи ставки: {e}\n{traceback.format_exc()}")


def handicap_result_table(match_id, teams_ID, handicap):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT period, handicap FROM mlb_handicap_bet WHERE match_id = %s", (match_id,))
    periods = cur.fetchall()

    for period in periods:

        value = getDictionary(period[0], handicap)

        if 0 < value[0] - value[1] + period[1]:
            team1_result = 'win'
        elif 0 == value[0] - value[1] + period[1]:
            team1_result = 'draw'
        else:
            team1_result = 'lose'

        if period[1] > 0:
            handi = -period[1]
        elif period[1] < 0:
            handi = abs(period[1])
        else:
            handi = period[1]

        if 0 < value[1] - value[0] + handi:
            team2_result = 'win'
        elif 0 == value[1] - value[0] + handi:
            team2_result = 'draw'
        else:
            team2_result = 'lose'

        cur.execute(f'''UPDATE mlb_handicap_bet SET handicap_team1_result = '{team1_result}', handicap_team2_result = '{team2_result}' WHERE match_id = '{match_id}' AND period = '{period[0]}' AND handicap = {period[1]};''')
        conn.commit()

