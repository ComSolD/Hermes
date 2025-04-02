def calculate_statistic_display(statistic_values, mode):
    if not statistic_values:
        return None

    if mode == "avg":
        return round(sum(statistic_values) / len(statistic_values), 2)
    elif mode == "list":
        return statistic_values
    elif mode == "overdrawunder":
        from collections import Counter
        counts = Counter(statistic_values)

        # Отображаем в читаемом порядке
        result = []
        for key in ["Больше", "Равно", "Меньше"]:
            if key in counts:
                result.append(f"{key} — {counts[key]} раз(а)")
        return result
    elif mode == "windrawlose":
        from collections import Counter
        counts = Counter(statistic_values)

        # Отображаем в читаемом порядке
        result = []
        for key in ["Победа", "Ничья", "Поражение"]:
            if key in counts:
                result.append(f"{key} — {counts[key]} раз(а)")
        return result


def handle_statistic_data(statistic_data, matches, data, player_id=None):
    from nba.models import (
        NBATeamPtsStat,
        NBAPlayerStat,
        NBATotalBet,
        NBAHandicapBet,
        NBAMatch,
    )

    if not statistic_data or not isinstance(statistic_data, dict):
        return []

    model = statistic_data.get("model")
    fields = statistic_data.get("fields", [])
    aggregate = statistic_data.get("aggregate", "team")
    threshold = float(statistic_data.get("threshold", 0))

    match_ids = list(matches.values_list("match_id", flat=True))
    team_id = data.get("team_id")

    match_stat_map = {mid: 0 for mid in match_ids}

    if model == "NBATeamPtsStat":
        stat_queryset = NBATeamPtsStat.objects.filter(match_id__in=match_ids)

        for stat in stat_queryset:
            if str(stat.team_id) != team_id:
                continue
            total = sum([getattr(stat, f, 0) or 0 for f in fields])
            match_stat_map[stat.match_id] += total

        return [match_stat_map[mid] for mid in match_ids if mid in match_stat_map]

    elif model == "NBAPlayerStat":
        stat_queryset = NBAPlayerStat.objects.filter(match_id__in=match_ids)

        for stat in stat_queryset:
            if str(stat.team_id) != team_id:
                continue
            if aggregate == "player" and player_id and str(stat.player_id) != player_id:
                continue
            total = sum([getattr(stat, f, 0) or 0 for f in fields])
            match_stat_map[stat.match_id] += total

        return [match_stat_map[mid] for mid in match_ids if mid in match_stat_map]

    elif model == "NBATotalBet" and "total" in fields:
        stat_queryset = NBATotalBet.objects.filter(match_id__in=match_ids, period=aggregate)

        RESULT_CHOICES = {
            "over": "Больше",
            "under": "Меньше",
            "draw": "Равно"
        }

        return [
            RESULT_CHOICES.get(stat.total_result, stat.total_result)
            for stat in stat_queryset
            if float(stat.total) == threshold
        ]
    elif model == "NBATotalBet" and "over_odds" in fields:
        threshold = float(threshold)
        rounded = round(threshold, 1)
        lower_bound = rounded
        upper_bound = rounded + 0.09

        stat_queryset = NBATotalBet.objects.filter(
            match_id__in=match_ids,
            period=aggregate,
            over_odds__gte=lower_bound,
            over_odds__lt=upper_bound
        ).order_by("match_id")  # можно убрать сортировку если не нужна

        RESULT_CHOICES = {
            "over": "Больше",
            "under": "Меньше",
            "draw": "Равно"
        }

        matched_results = []

        for stat in stat_queryset:
            matched_results.append(RESULT_CHOICES.get(stat.total_result, stat.total_result))

        return matched_results
    
    elif model == "NBATotalBet" and "under_odds" in fields:
        threshold = float(threshold)
        rounded = round(threshold, 1)
        lower_bound = rounded
        upper_bound = rounded + 0.09

        stat_queryset = NBATotalBet.objects.filter(
            match_id__in=match_ids,
            period=aggregate,
            under_odds__gte=lower_bound,
            under_odds__lt=upper_bound
        ).order_by("match_id")  # можно убрать сортировку если не нужна

        RESULT_CHOICES = {
            "over": "Больше",
            "under": "Меньше",
            "draw": "Равно"
        }

        matched_results = []

        for stat in stat_queryset:
            matched_results.append(RESULT_CHOICES.get(stat.total_result, stat.total_result))

        return matched_results

    elif model == "NBAHandicapBet" and "handicap" in fields:
        match_team_map = {
            match_id: (team1_id, team2_id)
            for match_id, team1_id, team2_id in NBAMatch.objects
                .filter(match_id__in=match_ids)
                .values_list("match_id", "team1_id", "team2_id")
        }

        stat_queryset = NBAHandicapBet.objects.filter(match_id__in=match_ids, period=aggregate)

        RESULT_CHOICES = {
            "win": "Победа",
            "lose": "Поражение",
            "draw": "Ничья"
        }

        values = []

        for stat in stat_queryset:
            match_teams = match_team_map.get(stat.match_id)
            if not match_teams:
                continue

            team1_id, team2_id = match_teams
            adjusted_handicap, result = None, None

            if str(team_id) == str(team1_id):
                adjusted_handicap = -stat.handicap
                result = stat.handicap_team1_result
            elif str(team_id) == str(team2_id):
                adjusted_handicap = stat.handicap
                result = stat.handicap_team2_result
            else:
                continue

            if adjusted_handicap == threshold:
                values.append(RESULT_CHOICES.get(result, result))

        return values

    return []
