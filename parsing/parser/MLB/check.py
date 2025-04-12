import numpy as np
import psycopg2
import configparser
import re
from datetime import datetime, timedelta
from thefuzz import fuzz, process

def total_check(totals):
    hit_team1 = int(totals[int(len(totals)/2)-2])
    hit_team2 = int(totals[-2])
    
    error_team1 = int(totals[int(len(totals)/2-1)])
    error_team2 = int(totals[-1])

    if totals[0] == '-':
        inning1_team1 = 0
    else:
        inning1_team1 = int(totals[0])
    if totals[1] == '-':
        inning2_team1 = 0
    else:
        inning2_team1 = int(totals[1])
    if totals[2] == '-':
        inning3_team1 = 0
    else:
        inning3_team1 = int(totals[2])
    if totals[3] == '-':
        inning4_team1 = 0
    else:
        inning4_team1 = int(totals[3])
    if totals[4] == '-':
        inning5_team1 = 0
    else:
        inning5_team1 = int(totals[4])
    if totals[5] == '-':
        inning6_team1 = 0
    else:
        inning6_team1 = int(totals[5])
    if totals[6] == '-':
        inning7_team1 = 0
    else:
        inning7_team1 = int(totals[6])
    if totals[7] == '-':
        inning8_team1 = 0
    else:
        inning8_team1 = int(totals[7])
    if totals[8] == '-':
        inning9_team1 = 0
    else:
        inning9_team1 = int(totals[8])

    if totals[int(len(totals)/2)] == '-':
        missed_inning1_team1 = 0
    else:
        missed_inning1_team1 = int(totals[int(len(totals)/2)])
    if totals[int(len(totals)/2)+1] == '-':
        missed_inning2_team1 = 0
    else:
        missed_inning2_team1 = int(totals[int(len(totals)/2)+1])
    if totals[int(len(totals)/2)+2] == '-':
        missed_inning3_team1 = 0
    else:
        missed_inning3_team1 = int(totals[int(len(totals)/2)+2])
    if totals[int(len(totals)/2)+3] == '-':
        missed_inning4_team1 = 0
    else:
        missed_inning4_team1 = int(totals[int(len(totals)/2)+3])
    if totals[int(len(totals)/2)+4] == '-':
        missed_inning5_team1 = 0
    else:
        missed_inning5_team1 = int(totals[int(len(totals)/2)+4])
    if totals[int(len(totals)/2)+5] == '-':
        missed_inning6_team1 = 0
    else:
        missed_inning6_team1 = int(totals[int(len(totals)/2)+5])
    if totals[int(len(totals)/2)+6] == '-':
        missed_inning7_team1 = 0
    else:
        missed_inning7_team1 = int(totals[int(len(totals)/2)+6])
    if totals[int(len(totals)/2)+7] == '-':
        missed_inning8_team1 = 0
    else:
        missed_inning8_team1 = int(totals[int(len(totals)/2)+7])
    if totals[int(len(totals)/2)+8] == '-':
        missed_inning9_team1 = 0
    else:
        missed_inning9_team1 = int(totals[int(len(totals)/2)+8])
    


    if totals[int(len(totals)/2)] == '-':
        inning1_team2 = 0
    else:
        inning1_team2 = int(totals[int(len(totals)/2)])
    if totals[int(len(totals)/2)+1] == '-':
        inning2_team2 = 0
    else:
        inning2_team2 = int(totals[int(len(totals)/2)+1])
    if totals[int(len(totals)/2)+2] == '-':
        inning3_team2 = 0
    else:
        inning3_team2 = int(totals[int(len(totals)/2)+2])
    if totals[int(len(totals)/2)+3] == '-':
        inning4_team2 = 0
    else:
        inning4_team2 = int(totals[int(len(totals)/2)+3])
    if totals[int(len(totals)/2)+4] == '-':
        inning5_team2 = 0
    else:
        inning5_team2 = int(totals[int(len(totals)/2)+4])
    if totals[int(len(totals)/2)+5] == '-':
        inning6_team2 = 0
    else:
        inning6_team2 = int(totals[int(len(totals)/2)+5])
    if totals[int(len(totals)/2)+6] == '-':
        inning7_team2 = 0
    else:
        inning7_team2 = int(totals[int(len(totals)/2)+6])
    if totals[int(len(totals)/2)+7] == '-':
        inning8_team2 = 0
    else:
        inning8_team2 = int(totals[int(len(totals)/2)+7])
    if totals[int(len(totals)/2)+8] == '-':
        inning9_team2 = 0
    else:
        inning9_team2 = int(totals[int(len(totals)/2)+8])

    if totals[0] == '-':
        missed_inning1_team2 = 0
    else:
        missed_inning1_team2 = int(totals[0])
    if totals[1] == '-':
        missed_inning2_team2 = 0
    else:
        missed_inning2_team2 = int(totals[1])
    if totals[2] == '-':
        missed_inning3_team2 = 0
    else:
        missed_inning3_team2 = int(totals[2])
    if totals[3] == '-':
        missed_inning4_team2 = 0
    else:
        missed_inning4_team2 = int(totals[3])
    if totals[4] == '-':
        missed_inning5_team2 = 0
    else:
        missed_inning5_team2 = int(totals[4])
    if totals[5] == '-':
        missed_inning6_team2 = 0
    else:
        missed_inning6_team2 = int(totals[5])
    if totals[6] == '-':
        missed_inning7_team2 = 0
    else:
        missed_inning7_team2 = int(totals[6])
    if totals[7] == '-':
        missed_inning8_team2 = 0
    else:
        missed_inning8_team2 = int(totals[7])
    if totals[8] == '-':
        missed_inning9_team2 = 0
    else:
        missed_inning9_team2 = int(totals[8])

    run_team1 = int(totals[int(len(totals)/2)-3])
    run_team2 = int(totals[-3])

    missed_hit_team1 = hit_team2
    missed_hit_team2 = hit_team1

    missed_run_team1 = run_team2
    missed_run_team2 = run_team1

    return [inning1_team1, missed_inning1_team1, inning2_team1, missed_inning2_team1, inning3_team1, missed_inning3_team1, inning4_team1, missed_inning4_team1, inning5_team1, missed_inning5_team1, inning6_team1, missed_inning6_team1, inning7_team1, missed_inning7_team1, inning8_team1, missed_inning8_team1, inning9_team1, missed_inning9_team1, error_team1, hit_team1, missed_hit_team1, run_team1, missed_run_team1], [inning1_team2, missed_inning1_team2, inning2_team2, missed_inning2_team2, inning3_team2, missed_inning3_team2, inning4_team2, missed_inning4_team2, inning5_team2, missed_inning5_team2, inning6_team2, missed_inning6_team2, inning7_team2, missed_inning7_team2, inning8_team2, missed_inning8_team2, inning9_team2, missed_inning9_team2, error_team2, hit_team2, missed_hit_team2, run_team2, missed_run_team2], [totals[int(len(totals)/2)-3], int(totals[-3])]


def stage_check(stages):
    if not stages:
        return "regular"
    
    
    stages = set(word.lower() for stage in stages for word in stage.split())

    # Особый случай для makeup
    if 'makeup' in stages and not {'alwc', 'nlwc', 'nlds', 'alds', 'nlcs', 'alcs', 'world', 'wild'}.intersection(stages):
        return "regular"
    
    # Карта матчей для быстрого поиска
    stage_mapping = {
        ('mlb', 'world', 'tour:'): "world tour",
        ('all-star',): "all-star",
        ('alwc',): "alwc",
        ('nlwc',): "nlwc",
        ('nlds',): "nlds",
        ('alds',): "alds",
        ('nlcs',): "nlcs",
        ('alcs',): "alcs",
        ('world', 'series'): "world series",
        ('wild', 'al'): "alwc",
        ('wild', 'nl'): "nlwc"
    }
    
    # Проверяем соответствие шаблонам
    for keys, value in stage_mapping.items():
        if set(keys).issubset(stages):
            return value
        
    
    return "regular"


def check_stat(player_names, player_stats, player_roles, player_IDs):
    while('' in player_stats):
        player_stats.remove('')

    pitcher_stat_team2 = list()

    for num in range(8):
        if num == 0:
            pcst = player_stats.pop(-1)
            pcst = pcst.split('-')
            pitcher_stat_team2.append(pcst[1])
            pitcher_stat_team2.append(pcst[0])
        else:
            pitcher_stat_team2.append(player_stats.pop(-1))

    pitcher_stat_team2.reverse()


    redact_list = list()


    while True:
        if '.' not in player_stats[-1] and player_stats[-1] != '---' and player_stats[-1] != 'INF':
            break
        else:
            check_null = player_stats.pop(-9)
            if check_null == '--':
                player_stats.pop(-8)
                player_stats.pop(-7)
                player_stats.pop(-6)
                player_stats.pop(-5)
                player_stats.pop(-4)
                player_stats.pop(-3)
                player_stats.pop(-2)
                player_stats.pop(-1)
            else:
                redact_list.append(check_null)
                redact_list.append(player_stats.pop(-8))
                redact_list.append(player_stats.pop(-7))
                redact_list.append(player_stats.pop(-6))
                redact_list.append(player_stats.pop(-5))
                redact_list.append(player_stats.pop(-4))
                redact_list.append(player_stats.pop(-3))

                pc_pitcher = player_stats.pop(-2)
                pc_pitcher = pc_pitcher.split('-')
                redact_list.append(pc_pitcher[0])
                redact_list.append(pc_pitcher[1])

                era_check = player_stats.pop(-1)
                if era_check == '---'or era_check == 'INF':
                    redact_list.append(0)
                else:
                    redact_list.append(era_check)

    redact_list.reverse()

    redact_list = np.array_split(redact_list, len(redact_list) / 10)

    pitcher_player_stat_team2 = list()

    for red in redact_list:
        lst = list(red)
        pitcher_player_stat_team2.append(lst)

    pitcher_player_stat_team2.reverse()

    for num in range(len(pitcher_player_stat_team2)):
        pitcher_player_stat_team2[num].reverse()
        pitcher_player_stat_team2[num].append(player_names.pop(-1))
        pitcher_player_stat_team2[num].append(player_IDs.pop(-1))

    pitcher_stat_team1 = list()

    for num in range(8):
        if num == 0:
            pcst = player_stats.pop(-1)
            pcst = pcst.split('-')
            pitcher_stat_team1.append(pcst[1])
            pitcher_stat_team1.append(pcst[0])
        else:
            pitcher_stat_team1.append(player_stats.pop(-1))

    pitcher_stat_team1.reverse()

    
    redact_list = list()


    while True:
        if '.' not in player_stats[-1] and player_stats[-1] != '---' and player_stats[-1] != 'INF':
            break
        else:
            check_null = player_stats.pop(-9)
            if check_null == '--':
                player_stats.pop(-8)
                player_stats.pop(-7)
                player_stats.pop(-6)
                player_stats.pop(-5)
                player_stats.pop(-4)
                player_stats.pop(-3)
                player_stats.pop(-2)
                player_stats.pop(-1)
            else:
                redact_list.append(check_null)
                redact_list.append(player_stats.pop(-8))
                redact_list.append(player_stats.pop(-7))
                redact_list.append(player_stats.pop(-6))
                redact_list.append(player_stats.pop(-5))
                redact_list.append(player_stats.pop(-4))
                redact_list.append(player_stats.pop(-3))

                pc_pitcher = player_stats.pop(-2)
                pc_pitcher = pc_pitcher.split('-')
                redact_list.append(pc_pitcher[0])
                redact_list.append(pc_pitcher[1])

                era_check = player_stats.pop(-1)
                if era_check == '---'or era_check == 'INF':
                    redact_list.append(0)
                else:
                    redact_list.append(era_check)

    redact_list.reverse()

    redact_list = np.array_split(redact_list, len(redact_list) / 10)

    pitcher_player_stat_team1 = list()

    for red in redact_list:
        lst = list(red)
        pitcher_player_stat_team1.append(lst)

    pitcher_player_stat_team1.reverse()

    for num in range(len(pitcher_player_stat_team1)):
        pitcher_player_stat_team1[num].reverse()
        pitcher_player_stat_team1[num].append(player_names.pop(-1))
        pitcher_player_stat_team1[num].append(player_IDs.pop(-1))


    hitter_stat_team2 = list()

    for num in range(7):
        hitter_stat_team2.append(player_stats.pop(-1))

    hitter_stat_team2.reverse()


    redact_list = list()

    while True:
        if '.' not in player_stats[7] and player_stats[7] != '--':
            break
        else:
            check_error = player_stats.pop(9)
            if check_error == '--':
                player_stats.pop(8)
                player_stats.pop(7)
                player_stats.pop(6)
                player_stats.pop(5)
                player_stats.pop(4)
                player_stats.pop(3)
                player_stats.pop(2)
                player_stats.pop(1)
                player_stats.pop(0)
            else:
                redact_list.append(check_error)
                redact_list.append(player_stats.pop(8))
                redact_list.append(player_stats.pop(7))
                redact_list.append(player_stats.pop(6))
                redact_list.append(player_stats.pop(5))
                redact_list.append(player_stats.pop(4))
                redact_list.append(player_stats.pop(3))
                redact_list.append(player_stats.pop(2))
                redact_list.append(player_stats.pop(1))
                redact_list.append(player_stats.pop(0))

    redact_list.reverse()

    redact_list = np.array_split(redact_list, len(redact_list) / 10)

    hitter_player_stat_team1 = list()

    for red in redact_list:
        lst = list(red)
        hitter_player_stat_team1.append(lst)

    hitter_player_stat_team1.reverse()


    for num in range(len(hitter_player_stat_team1)):
        hitter_player_stat_team1[num].append(player_names.pop(0))
        hitter_player_stat_team1[num].append(player_roles.pop(0))
        hitter_player_stat_team1[num].append(player_IDs.pop(0))

    
    hitter_stat_team1 = list()

    for num in range(7):
        hitter_stat_team1.append(player_stats.pop(0))

    redact_list = list()
    
    while len(player_stats) != 0:
        check_error = player_stats.pop(9)
        if check_error == '--':
            player_stats.pop(8)
            player_stats.pop(7)
            player_stats.pop(6)
            player_stats.pop(5)
            player_stats.pop(4)
            player_stats.pop(3)
            player_stats.pop(2)
            player_stats.pop(1)
            player_stats.pop(0)
        else:
            redact_list.append(check_error)
            redact_list.append(player_stats.pop(8))
            redact_list.append(player_stats.pop(7))
            redact_list.append(player_stats.pop(6))
            redact_list.append(player_stats.pop(5))
            redact_list.append(player_stats.pop(4))
            redact_list.append(player_stats.pop(3))
            redact_list.append(player_stats.pop(2))
            redact_list.append(player_stats.pop(1))
            redact_list.append(player_stats.pop(0))

    redact_list.reverse()

    redact_list = np.array_split(redact_list, len(redact_list)/10)

    hitter_player_stat_team2 = list()

    for red in redact_list:
        lst = list(red)
        hitter_player_stat_team2.append(lst)

    hitter_player_stat_team2.reverse()

    for num in range(len(hitter_player_stat_team2)):
        hitter_player_stat_team2[num].append(player_names.pop(0))
        hitter_player_stat_team2[num].append(player_roles.pop(0))
        hitter_player_stat_team2[num].append(player_IDs.pop(0))

    return pitcher_player_stat_team1, pitcher_player_stat_team2, hitter_player_stat_team1, hitter_player_stat_team2


def extract_time(match_id):
    """Извлекает время из match_id в формате HH:MM."""
    time_match = re.search(r'_(\d{2}_\d{2})$', match_id)
    return time_match.group(1).replace('_', ':') if time_match else None


def find_closest_match(db_matches, search_time):
    """Находит ближайший match_id с минимальной разницей во времени."""


    search_dt = datetime.strptime(search_time, "%H:%M")

    min_diff = timedelta.max
    closest_match = None


    for match_id in db_matches:
        match_time = extract_time(match_id)

        if match_time:
            match_dt = datetime.strptime(match_time, "%H:%M")
            diff = abs(search_dt - match_dt)
            
            if diff < min_diff:
                min_diff = diff
                closest_match = match_id

    return closest_match


def id_check(match_id, search_time):
    """Поиск ближайшего match_id в базе данных с учетом разницы во времени."""
    # Читаем конфигурацию БД
    config = configparser.ConfigParser()
    config.read("config.ini")
    db_params = config["postgresql"]
    
    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    try:
        # Формируем основную часть match_id без времени
        
        # SQL-запрос для поиска матчей с нужным префиксом
        cur.execute("""SELECT match_id FROM mlb_match WHERE match_id LIKE %s""", (match_id,))
        
        # Получаем все найденные match_id
        db_matches = [row[0] for row in cur.fetchall()]
        
        if not db_matches:
            return None  # Нет совпадений
        
        
        # Находим ближайший match_id по времени
        best_match = find_closest_match(db_matches, search_time)
        
        return best_match
    
    finally:
        cur.close()
        conn.close()


def get_best_match(input_name, team_names):
    """ Возвращает название команды и ID с наибольшим совпадением """
    best_match = process.extractOne(
        input_name, 
        team_names.keys(), 
        scorer=fuzz.partial_ratio  # Используем partial_ratio для учета частичных совпадений
    )

    if best_match and best_match[1] > 70:  # Снижен порог на 70%
        return team_names[best_match[0]], best_match[0]  # Возвращаем (team_id, team_name)
    else:
        return None, None  # Если совпадения нет


def team_check(name_team1, name_team2):
    # Загружаем конфиг
    config = configparser.ConfigParser()
    config.read("config.ini")
    db_params = config["postgresql"]

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Получаем все команды
    cur.execute("SELECT team_id, name FROM mlb_team;")
    teams = cur.fetchall()

    # Создаем словарь {team_name: team_id}
    team_dict = {name: team_id for team_id, name in teams}

    # Поиск ближайшего совпадения
    team1_id, team1_name = get_best_match(name_team1, team_dict)
    team2_id, team2_name = get_best_match(name_team2, team_dict)

    if not team1_id or not team2_id:
        return f"Одна или обе команды не найдены: {name_team1}, {name_team2}"

    return team1_id, team2_id, team1_name, team2_name
