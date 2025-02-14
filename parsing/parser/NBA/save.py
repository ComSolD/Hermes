from datetime import datetime
from unittest import result
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


def bet_predict_tables(match_id, teams_id, bet_predict):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    bet_id = str(uuid.uuid4())

    cur.execute(f'''INSERT INTO nba_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_id}', '{match_id}', '{teams_id[0]}', '{teams_id[1]}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})''')
    conn.commit()


def bet_result_tables(match_id, teams, resul_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nba_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nba_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nba_bet WHERE match_id = '{match_id}';")
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


        cur.execute(f'''UPDATE nba_bet SET ml_result = '{teams[0] if resul_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
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
            

        cur.execute(f'''INSERT INTO nba_bet(bet_id, match_id, team1_id, team2_id, ml_team1_parlay, ml_team2_parlay, ml_result, total, over_total_parlay, under_total_parlay, total_result, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay, spread_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', {bet[0]}, {bet[1]},'{teams[0] if resul_team1 == "Win" else teams[1]}', {bet[2]}, {bet[3]}, {bet[4]}, '{'over' if float(bet[2]) < (int(match_total[0]) + int(match_total[1])) else 'under'}', {bet[5]}, {bet[6]}, {bet[7]}, {bet[8]}, '{spread_team}');''')
        conn.commit()


def bet_old_result_tables(match_id, teams, resul_team1, match_total, bet):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Получаем параметры подключения
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()


    cur.execute(f"SELECT match_id FROM nba_bet WHERE match_id = '{match_id}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT total FROM nba_bet WHERE match_id = '{match_id}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT spread_team1 FROM nba_bet WHERE match_id = '{match_id}';")
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


        cur.execute(f'''UPDATE nba_bet SET ml_result = '{teams[0] if resul_team1 == "Win" else teams[1]}', total_result = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_result = '{spread_team}' WHERE match_id = '{match_id}';''')
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

            
        cur.execute(f'''INSERT INTO nba_bet(bet_id, match_id, team1_id, team2_id, ml_result, total, total_result, spread_team1, spread_team2, spread_result) VALUES('{bet_id}', '{match_id}', '{teams[0]}', '{teams[1]}', '{teams[0] if resul_team1 == "Win" else teams[1]}', {bet[2]}, '{'over' if bet[2] < (int(match_total[0]) + int(match_total[1])) else 'under'}', '{team1_spread}', '{team2_spread}', '{spread_team}');''')
        conn.commit()
 

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

        cur.execute(f'''INSERT INTO nba_player_stat(stat_id, player_id, match_id ,team_id , position, pts, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf, plus_minus, min) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Starter', {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
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

        cur.execute(f'''INSERT INTO nba_player_stat(stat_id, player_id, match_id ,team_id , position, pts, fg, trying_fg, three_pt, attempted_three_pt, ft, trying_ft, oreb, dreb, reb, ast, stl, blk, turnovers, pf, plus_minus, min) VALUES('{stat_id}', '{player_id}', '{match_id}', '{team_id}', 'Bench', {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
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
        

    if not exists:

        cur.execute(f"INSERT INTO nba_match(match_id, team1_id, team2_id, season, date) VALUES('{match_id}', '{teams[0]}', '{teams[1]}', '{season}', '{date_match}')")
        conn.commit()

        return False
    
    elif exists and stage_check[0] is None:


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

        cur.execute(f"INSERT INTO nba_total_bet(total_bet_id, match_id, total, over_odds, under_odds, period) VALUES('{bet_id}', '{match_id}', {odd[0]}, {odd[1]}, {odd[2]}, '{period}')")
        conn.commit()


def total_result_table(match_id, teams_ID, total):
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
