import numpy as np
import psycopg2
import configparser
import re
from datetime import datetime, timedelta
from thefuzz import fuzz, process


def total_check(totals):
    totals.pop(int(len(totals)/2))
    totals.pop(0)

    quarter1_team1 = int(totals[0])
    quarter2_team1 = int(totals[1])
    quarter3_team1 = int(totals[2])
    quarter4_team1 = int(totals[3])
    missed_quarter1_team1 = int(totals[int(len(totals)/2)])
    missed_quarter2_team1 = int(totals[int(len(totals)/2)+1])
    missed_quarter3_team1 = int(totals[int(len(totals)/2)+2])
    missed_quarter4_team1 = int(totals[int(len(totals)/2)+3])
    total_team1 = quarter1_team1 + quarter2_team1 + quarter3_team1 + quarter4_team1

    quarter1_team2 = int(totals[int(len(totals)/2)])
    quarter2_team2 = int(totals[int(len(totals)/2)+1])
    quarter3_team2 = int(totals[int(len(totals)/2)+2])
    quarter4_team2 = int(totals[int(len(totals)/2)+3])
    missed_quarter1_team2 = int(totals[0])
    missed_quarter2_team2 = int(totals[1])
    missed_quarter3_team2 = int(totals[2])
    missed_quarter4_team2 = int(totals[3])
    total_team2 = quarter1_team2 + quarter2_team2 + quarter3_team2 + quarter4_team2

    missed_total_team1 = total_team2
    missed_total_team2 = total_team1

    return [quarter1_team1, missed_quarter1_team1, quarter2_team1, missed_quarter2_team1, quarter3_team1, missed_quarter3_team1, quarter4_team1, missed_quarter4_team1, total_team1, missed_total_team1], [quarter1_team2, missed_quarter1_team2, quarter2_team2, missed_quarter2_team2, quarter3_team2, missed_quarter3_team2, quarter4_team2, missed_quarter4_team2, total_team2, missed_total_team2], [totals[int(len(totals)/2-1)], totals[-1]]


def stage_check(stages):

    if not stages:
        return "regular"
    
    stages = set(word.lower() for stage in stages for word in stage.split())

    # Обрабатываем особые случаи
    if {'rising', 'stars'}.issubset(stages):
        return 0
    if {'makeup'}.issubset(stages) and not {'east', 'west', 'finals'}.intersection(stages):
        return "regular"

    # Карта матчей для быстрого поиска
    stage_mapping = {
        ('all-star',): "all-star",
        ('preseason',): "preseason",
        ('nba', 'finals'): "nba finals",
        ('east', 'finals'): "east finals",
        ('west', 'finals'): "west finals",
        ('east', 'semifinals'): "east semifinals",
        ('west', 'semifinals'): "west semifinals",
        ('east', '1st', 'round'): "east 1st round",
        ('west', '1st', 'round'): "west 1st round",
        ('play-in', 'east', '9th', '10th'): "play-in east 9th place vs 10th place",
        ('play-in', 'west', '9th', '10th'): "play-in west 9th place vs 10th place",
        ('play-in', 'east', '7th', '8th'): "play-in east 7th place vs 8th place",
        ('play-in', 'west', '7th', '8th'): "play-in west 7th place vs 8th place",
        ('play-in', 'east', '8th', 'seed'): "play-in east 8th seed",
        ('play-in', 'west', '8th', 'seed'): "play-in west 8th seed",
        ('in-season', 'quarterfinals'): "in-season quarterfinals",
        ('in-season', 'semifinals'): "in-season semifinals",
        ('in-season', 'championship'): "in-season championship"
    }

    # Проверяем соответствие шаблонам
    for keys, value in stage_mapping.items():
        if set(keys).issubset(stages):
            return value

    return "regular"


def check_stat(player_names, player_stats, player_IDs):
    while('' in player_stats):
        player_stats.remove('')

    num = 0

    redact_list = [[],[],[],[]]

    for i in player_stats:
        if i == 'MIN':
            num += 1
        redact_list[num-1].append(i)
    
    

    for i in range(len(redact_list)):
        redact_list[i].remove('MIN')
        redact_list[i].remove('FG')
        redact_list[i].remove('3PT')
        redact_list[i].remove('FT')
        redact_list[i].remove('OREB')
        redact_list[i].remove('DREB')
        redact_list[i].remove('REB')
        redact_list[i].remove('AST')
        redact_list[i].remove('STL')
        redact_list[i].remove('BLK')
        redact_list[i].remove('TO')
        redact_list[i].remove('PF')
        redact_list[i].remove('+/-')
        redact_list[i].remove('PTS')

    redact_list[3].pop(-3)
    redact_list[3].pop(-2)
    redact_list[3].pop(-1)

    redact_list[1].pop(-3)
    redact_list[1].pop(-2)
    redact_list[1].pop(-1)

    # Общая статистика 1 команды
    stat_team1 = list()

    for stat in range(12):
        stat = redact_list[1].pop(-1)
        stat_team1.append(stat)

    stat_team1.reverse()

    stat_team1[0] = stat_team1[0].split('-')
    stat_team1[1] = stat_team1[1].split('-')
    stat_team1[2] = stat_team1[2].split('-')


    # Общая статистика 2 команды
    stat_team2 = list()

    for stat in range(12):
        stat = redact_list[3].pop(-1)
        stat_team2.append(stat)

    stat_team2.reverse()

    stat_team2[0] = stat_team2[0].split('-')
    stat_team2[1] = stat_team2[1].split('-')
    stat_team2[2] = stat_team2[2].split('-')

    # Редактируем и записывае скамейку 2 команды
    num_DNP = 0

    for DNP in redact_list[3]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[3].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[3] = np.array_split(redact_list[3],len(redact_list[3])/14)

    bench_team2 = list()

    for array in redact_list[3]:
        bench = list(array)
        bench[1] = bench[1].split('-')
        bench[2] = bench[2].split('-')
        bench[3] = bench[3].split('-')
        bench_team2.append(bench)


    for num_player in range(len(bench_team2), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        bench_team2[-num_player].append(player)
        bench_team2[-num_player].append(IDs)


    # Запись данных в массив стартера 2 команды
    num_DNP = 0

    for DNP in redact_list[2]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[2].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[2] = np.array_split(redact_list[2],len(redact_list[2])/14)

    starter_team2 = list()

    for array in redact_list[2]:
        starter = list(array)
        starter[1] = starter[1].split('-')
        starter[2] = starter[2].split('-')
        starter[3] = starter[3].split('-')
        starter_team2.append(starter)


    for num_player in range(len(starter_team2), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        starter_team2[-num_player].append(player)
        starter_team2[-num_player].append(IDs)


    # Редактируем и записывае скамейку 1 команды
    num_DNP = 0

    for DNP in redact_list[1]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[1].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[1] = np.array_split(redact_list[1],len(redact_list[1])/14)

    bench_team1 = list()

    for array in redact_list[1]:
        bench = list(array)
        bench[1] = bench[1].split('-')
        bench[2] = bench[2].split('-')
        bench[3] = bench[3].split('-')
        bench_team1.append(bench)


    for num_player in range(len(bench_team1), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        bench_team1[-num_player].append(player)
        bench_team1[-num_player].append(IDs)

    
    # Запись данных в массив стартера 1 команды
    num_DNP = 0

    for DNP in redact_list[0]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[0].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[0] = np.array_split(redact_list[0],len(redact_list[0])/14)

    starter_team1 = list()

    for array in redact_list[0]:
        starter = list(array)
        starter[1] = starter[1].split('-')
        starter[2] = starter[2].split('-')
        starter[3] = starter[3].split('-')
        starter_team1.append(starter)


    for num_player in range(len(starter_team1), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        starter_team1[-num_player].append(player)
        starter_team1[-num_player].append(IDs)

    return stat_team1, stat_team2, starter_team1, starter_team2, bench_team1, bench_team2


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
        cur.execute("""SELECT match_id FROM nba_match WHERE match_id LIKE %s""", (match_id,))
        
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
    cur.execute("SELECT team_id, name FROM nba_team;")
    teams = cur.fetchall()

    # Создаем словарь {team_name: team_id}
    team_dict = {name: team_id for team_id, name in teams}

    # Поиск ближайшего совпадения
    team1_id, team1_name = get_best_match(name_team1, team_dict)
    team2_id, team2_name = get_best_match(name_team2, team_dict)

    if not team1_id or not team2_id:
        return f"Одна или обе команды не найдены: {name_team1}, {name_team2}"

    return team1_id, team2_id, team1_name, team2_name

