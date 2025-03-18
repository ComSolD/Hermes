import numpy as np
import psycopg2
import configparser
import re
from datetime import datetime, timedelta
from thefuzz import fuzz, process

def total_check(totals):
    totals.pop(int(len(totals)/2))
    totals.pop(0)

    third1_team1 = int(totals[0])
    third2_team1 = int(totals[1])
    third3_team1 = int(totals[2])
    missed_third1_team1 = int(totals[int(len(totals)/2)])
    missed_third2_team1 = int(totals[int(len(totals)/2)+1])
    missed_third3_team1 = int(totals[int(len(totals)/2)+2])
    total_team1 = third1_team1 + third2_team1 + third3_team1

    third1_team2 = int(totals[int(len(totals)/2)])
    third2_team2 = int(totals[int(len(totals)/2)+1])
    third3_team2 = int(totals[int(len(totals)/2)+2])
    missed_third1_team2 = int(totals[0])
    missed_third2_team2 = int(totals[1])
    missed_third3_team2 = int(totals[2])
    total_team2 = third1_team2 + third2_team2 + third3_team2

    missed_total_team1 = total_team2
    missed_total_team2 = total_team1

    return [third1_team1, missed_third1_team1, third2_team1, missed_third2_team1, third3_team1, missed_third3_team1, total_team1, missed_total_team1], [third1_team2, missed_third1_team2, third2_team2, missed_third2_team2, third3_team2, missed_third3_team2, total_team2, missed_total_team2], [totals[int(len(totals)/2-1)], totals[-1]]


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
        ('east', 'finals'): "east finals",
        ('west', 'finals'): "west finals",
        ('east', 'semifinals'): "east semifinals",
        ('west', 'semifinals'): "west semifinals",
        ('east', '1st', 'round'): "east 1st round",
        ('west', '1st', 'round'): "west 1st round",
        ('east', '2nd', 'round'): "east 2nd round",
        ('west', '2nd', 'round'): "west 2nd round",
        ('stanley', 'cup', 'final'): "stanley cup final",
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
        if i == 'FO%':
            num += 1
        redact_list[num-1].append(i)


    for i in range(len(redact_list)):
        redact_list[i].remove('G')
        redact_list[i].remove('A')
        redact_list[i].remove('+/-')
        redact_list[i].remove('S')
        redact_list[i].remove('SM')
        redact_list[i].remove('BS')
        redact_list[i].remove('PN')
        redact_list[i].remove('PIM')
        redact_list[i].remove('HT')
        redact_list[i].remove('TK')
        redact_list[i].remove('GV')
        redact_list[i].remove('SHFT')
        redact_list[i].remove('TOI')
        redact_list[i].remove('PPTOI')
        redact_list[i].remove('SHTOI')
        redact_list[i].remove('ESTOI')
        redact_list[i].remove('FW')
        redact_list[i].remove('FL')
        redact_list[i].remove('FO%')


    particular_value = "SA"

    arr = np.array(redact_list[3])
    
    idx = np.where(arr == particular_value)[0]
    
    subarrays = np.split(arr, idx)

    redact_list[3] = list(subarrays[0])


    goalies = list(subarrays[1])

    goalies.remove('SA')
    goalies.remove('GA')
    goalies.remove('SV')
    goalies.remove('SV%')
    goalies.remove('ESSV')
    goalies.remove('PPSV')
    goalies.remove('SHSV')
    goalies.remove('SOSA')
    goalies.remove('SOS')
    goalies.remove('TOI')
    goalies.remove('PIM')


    goalies = np.array_split(goalies,len(goalies)/11)

    goalies_team2 = list()

    for array in goalies:
        goalie = list(array)

        goalie.pop(6)
        goalie.pop(6)
        goalie.pop(6)
        goalie.pop(6)
    
        goalies_team2.append(goalie)

    goalies_team2.reverse()

    for num in range(len(goalies_team2)):
        goalies_team2[num].append(player_names.pop(-1))
        goalies_team2[num].append(player_IDs.pop(-1))

    goalies_team2.reverse()



    defensemen_team2 = list()

    redact_list[3] = np.array_split(redact_list[3],len(redact_list[3])/19)

    for array in redact_list[3]:
        forward = list(array)
        defensemen_team2.append(forward[0:11])

    if len(defensemen_team2) > 1:
        defensemen_team2.reverse()

        for num in range(len(defensemen_team2)):
            defensemen_team2[num].append(player_names.pop(-1))
            defensemen_team2[num].append(player_IDs.pop(-1))

        defensemen_team2.reverse()
    


    forwards_team2 = list()

    redact_list[2] = np.array_split(redact_list[2],len(redact_list[2])/19)

    for array in redact_list[2]:
        forward = list(array)
        forwards_team2.append(forward[0:11])

    if len(forwards_team2) > 1:
        forwards_team2.reverse()

        for num in range(len(forwards_team2)):
            forwards_team2[num].append(player_names.pop(-1))
            forwards_team2[num].append(player_IDs.pop(-1))

        forwards_team2.reverse()

    for defensemen in defensemen_team2:
        forwards_team2.append(defensemen)
    


    forwards_team1 = list()

    redact_list[0] = np.array_split(redact_list[0],len(redact_list[0])/19)

    for array in redact_list[0]:
        forward = list(array)
        forwards_team1.append(forward[0:11])

    if len(forwards_team1) > 1:

        for num in range(len(forwards_team1)):
            forwards_team1[num].append(player_names.pop(0))
            forwards_team1[num].append(player_IDs.pop(0))



    particular_value = "SA"

    arr = np.array(redact_list[1])
    
    idx = np.where(arr == particular_value)[0]
    
    subarrays = np.split(arr, idx)

    redact_list[1] = list(subarrays[0])


    goalies = list(subarrays[1])

    goalies.remove('SA')
    goalies.remove('GA')
    goalies.remove('SV')
    goalies.remove('SV%')
    goalies.remove('ESSV')
    goalies.remove('PPSV')
    goalies.remove('SHSV')
    goalies.remove('SOSA')
    goalies.remove('SOS')
    goalies.remove('TOI')
    goalies.remove('PIM')


    goalies = np.array_split(goalies,len(goalies)/11)

    goalies_team1 = list()

    for array in goalies:
        goalie = list(array)

        goalie.pop(6)
        goalie.pop(6)
        goalie.pop(6)
        goalie.pop(6)
    
        goalies_team1.append(goalie)

    goalies_team1.reverse()

    for num in range(len(goalies_team1)):
        goalies_team1[num].append(player_names.pop(-1))
        goalies_team1[num].append(player_IDs.pop(-1))

    goalies_team1.reverse()



    defensemen_team1 = list()

    redact_list[1] = np.array_split(redact_list[1],len(redact_list[1])/19)

    for array in redact_list[1]:
        forward = list(array)
        defensemen_team1.append(forward[0:11])

    if len(defensemen_team1) > 1:
        defensemen_team1.reverse()

        for num in range(len(defensemen_team1)):
            defensemen_team1[num].append(player_names.pop(-1))
            defensemen_team1[num].append(player_IDs.pop(-1))

        defensemen_team1.reverse()

    for defensemen in defensemen_team1:
        forwards_team1.append(defensemen)

    return forwards_team1, forwards_team2, defensemen_team1, defensemen_team2, goalies_team1, goalies_team2


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
        cur.execute("""SELECT match_id FROM nhl_match WHERE match_id LIKE %s""", (match_id,))
        
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
    cur.execute("SELECT team_id, name FROM nhl_team;")
    teams = cur.fetchall()

    # Создаем словарь {team_name: team_id}
    team_dict = {name: team_id for team_id, name in teams}

    # Поиск ближайшего совпадения
    team1_id, team1_name = get_best_match(name_team1, team_dict)
    team2_id, team2_name = get_best_match(name_team2, team_dict)

    if not team1_id or not team2_id:
        return f"Одна или обе команды не найдены: {name_team1}, {name_team2}"

    return team1_id, team2_id, team1_name, team2_name

