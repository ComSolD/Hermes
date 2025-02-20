import numpy as np


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
