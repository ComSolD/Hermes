import numpy as np

def total_check(totals):
    hit_team1 = int(totals[int(len(totals)/2)-2])
    hit_team2 = int(totals[-2])
    
    error_team1 = int(totals[int(len(totals)/2-1)])
    error_team2 = int(totals[-1])

    if totals[0] == '-':
        inning1_team1 = 'NULL'
    else:
        inning1_team1 = int(totals[0])
    if totals[1] == '-':
        inning2_team1 = 'NULL'
    else:
        inning2_team1 = int(totals[1])
    if totals[2] == '-':
        inning3_team1 = 'NULL'
    else:
        inning3_team1 = int(totals[2])
    if totals[3] == '-':
        inning4_team1 = 'NULL'
    else:
        inning4_team1 = int(totals[3])
    if totals[4] == '-':
        inning5_team1 = 'NULL'
    else:
        inning5_team1 = int(totals[4])
    if totals[5] == '-':
        inning6_team1 = 'NULL'
    else:
        inning6_team1 = int(totals[5])
    if totals[6] == '-':
        inning7_team1 = 'NULL'
    else:
        inning7_team1 = int(totals[6])
    if totals[7] == '-':
        inning8_team1 = 'NULL'
    else:
        inning8_team1 = int(totals[7])
    if totals[8] == '-':
        inning9_team1 = 'NULL'
    else:
        inning9_team1 = int(totals[8])

    if totals[int(len(totals)/2)] == '-':
        missed_inning1_team1 = 'NULL'
    else:
        missed_inning1_team1 = int(totals[int(len(totals)/2)])
    if totals[int(len(totals)/2)+1] == '-':
        missed_inning2_team1 = 'NULL'
    else:
        missed_inning2_team1 = int(totals[int(len(totals)/2)+1])
    if totals[int(len(totals)/2)+2] == '-':
        missed_inning3_team1 = 'NULL'
    else:
        missed_inning3_team1 = int(totals[int(len(totals)/2)+2])
    if totals[int(len(totals)/2)+3] == '-':
        missed_inning4_team1 = 'NULL'
    else:
        missed_inning4_team1 = int(totals[int(len(totals)/2)+3])
    if totals[int(len(totals)/2)+4] == '-':
        missed_inning5_team1 = 'NULL'
    else:
        missed_inning5_team1 = int(totals[int(len(totals)/2)+4])
    if totals[int(len(totals)/2)+5] == '-':
        missed_inning6_team1 = 'NULL'
    else:
        missed_inning6_team1 = int(totals[int(len(totals)/2)+5])
    if totals[int(len(totals)/2)+6] == '-':
        missed_inning7_team1 = 'NULL'
    else:
        missed_inning7_team1 = int(totals[int(len(totals)/2)+6])
    if totals[int(len(totals)/2)+7] == '-':
        missed_inning8_team1 = 'NULL'
    else:
        missed_inning8_team1 = int(totals[int(len(totals)/2)+7])
    if totals[int(len(totals)/2)+8] == '-':
        missed_inning9_team1 = 'NULL'
    else:
        missed_inning9_team1 = int(totals[int(len(totals)/2)+8])
    


    if totals[int(len(totals)/2)] == '-':
        inning1_team2 = 'NULL'
    else:
        inning1_team2 = int(totals[int(len(totals)/2)])
    if totals[int(len(totals)/2)+1] == '-':
        inning2_team2 = 'NULL'
    else:
        inning2_team2 = int(totals[int(len(totals)/2)+1])
    if totals[int(len(totals)/2)+2] == '-':
        inning3_team2 = 'NULL'
    else:
        inning3_team2 = int(totals[int(len(totals)/2)+2])
    if totals[int(len(totals)/2)+3] == '-':
        inning4_team2 = 'NULL'
    else:
        inning4_team2 = int(totals[int(len(totals)/2)+3])
    if totals[int(len(totals)/2)+4] == '-':
        inning5_team2 = 'NULL'
    else:
        inning5_team2 = int(totals[int(len(totals)/2)+4])
    if totals[int(len(totals)/2)+5] == '-':
        inning6_team2 = 'NULL'
    else:
        inning6_team2 = int(totals[int(len(totals)/2)+5])
    if totals[int(len(totals)/2)+6] == '-':
        inning7_team2 = 'NULL'
    else:
        inning7_team2 = int(totals[int(len(totals)/2)+6])
    if totals[int(len(totals)/2)+7] == '-':
        inning8_team2 = 'NULL'
    else:
        inning8_team2 = int(totals[int(len(totals)/2)+7])
    if totals[int(len(totals)/2)+8] == '-':
        inning9_team2 = 'NULL'
    else:
        inning9_team2 = int(totals[int(len(totals)/2)+8])

    if totals[0] == '-':
        missed_inning1_team2 = 'NULL'
    else:
        missed_inning1_team2 = int(totals[0])
    if totals[1] == '-':
        missed_inning2_team2 = 'NULL'
    else:
        missed_inning2_team2 = int(totals[1])
    if totals[2] == '-':
        missed_inning3_team2 = 'NULL'
    else:
        missed_inning3_team2 = int(totals[2])
    if totals[3] == '-':
        missed_inning4_team2 = 'NULL'
    else:
        missed_inning4_team2 = int(totals[3])
    if totals[4] == '-':
        missed_inning5_team2 = 'NULL'
    else:
        missed_inning5_team2 = int(totals[4])
    if totals[5] == '-':
        missed_inning6_team2 = 'NULL'
    else:
        missed_inning6_team2 = int(totals[5])
    if totals[6] == '-':
        missed_inning7_team2 = 'NULL'
    else:
        missed_inning7_team2 = int(totals[6])
    if totals[7] == '-':
        missed_inning8_team2 = 'NULL'
    else:
        missed_inning8_team2 = int(totals[7])
    if totals[8] == '-':
        missed_inning9_team2 = 'NULL'
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
        ('all-star',): "all-star",
        ('alwc',): "ALWC",
        ('nlwc',): "NLWC",
        ('nlds',): "NLDS",
        ('alds',): "ALDS",
        ('nlcs',): "NLCS",
        ('alcs',): "ALCS",
        ('world', 'series'): "world series",
        ('wild', 'al'): "ALWC",
        ('wild', 'nl'): "NLWC"
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
                    redact_list.append('NULL')
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
                    redact_list.append('NULL')
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
