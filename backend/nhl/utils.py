from collections import Counter
import statistics

def _display_avg(values):
    return round(sum(values) / len(values), 2)

def _display_list(values):
    return values

def _display_overdrawunder(values):
    counts = Counter(values)
    return [
        f"{label} — {counts[label]} раз(а)"
        for label in ["Больше", "Равно", "Меньше"]
        if label in counts
    ]

def _display_windrawlose(values):
    counts = Counter(values)
    return [
        f"{label} — {counts[label]} раз(а)"
        for label in ["Победа", "Ничья", "Поражение"]
        if label in counts
    ]

def _display_graph(values):
    return values


def _display_boxplot(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)

    if n == 0:
        return None

    q2 = statistics.median(sorted_vals)
    q1 = statistics.median(sorted_vals[:n//2])
    q3 = statistics.median(sorted_vals[(n+1)//2:])

    return {
        "min": sorted_vals[0],
        "q1": q1,
        "median": q2,
        "q3": q3,
        "max": sorted_vals[-1],
    }


# 👇 Главное обновление — регистр функций по режимам
DISPLAY_HANDLERS = {
    "avg": _display_avg,
    "list": _display_list,
    "overdrawunder": _display_overdrawunder,
    "windrawlose": _display_windrawlose,
    "graph": _display_graph,
    "boxplot": _display_boxplot,
}


def calculate_statistic_display(statistic_values, mode):
    if not statistic_values:
        return None

    handler = DISPLAY_HANDLERS.get(mode)
    if handler:
        return handler(statistic_values)

    return statistic_values  # fallback

def handle_statistic_data(statistic_data, matches, data, player_id=None):
    from nhl.models import (
        NHLTeamPtsStat,
        NHLPlayerStat,
        NHLTotalBet,
        NHLHandicapBet,
        NHLMatch,
        NHLMoneylineBet
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

    if model == "NHLTeamPtsStat":
        stat_queryset = NHLTeamPtsStat.objects.filter(match_id__in=match_ids)

        for stat in stat_queryset:
            if str(stat.team_id) != team_id:
                continue
            total = sum([getattr(stat, f, 0) or 0 for f in fields])
            match_stat_map[stat.match_id] += total

        return [match_stat_map[mid] for mid in match_ids if mid in match_stat_map]

    elif model == "NHLPlayerStat":
        stat_queryset = NHLPlayerStat.objects.filter(match_id__in=match_ids)

        for stat in stat_queryset:
            if team_id and str(stat.team_id) != str(team_id):
                continue

            if aggregate == "player" and player_id and str(stat.player_id) != player_id:
                continue
            total = sum([getattr(stat, f, 0) or 0 for f in fields])
            match_stat_map[stat.match_id] += total

        return [match_stat_map[mid] for mid in match_ids if mid in match_stat_map]
    
    elif model == "NHLMoneylineBet" and "result" in fields:
        stat_queryset = NHLMoneylineBet.objects.filter(match_id__in=match_ids, period=aggregate)

        matched_results = []

        for stat in stat_queryset:
            if str(stat.result) == str(team_id):
                matched_results.append("Победа")
            else:
                matched_results.append("Поражение")

        return matched_results

    elif model == "NHLTotalBet" and "total" in fields:
        stat_queryset = NHLTotalBet.objects.filter(match_id__in=match_ids, period=aggregate)

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
    elif model == "NHLTotalBet" and "over_odds" in fields:
        threshold = float(threshold)
        rounded = round(threshold, 1)
        lower_bound = rounded
        upper_bound = rounded + 0.09

        stat_queryset = NHLTotalBet.objects.filter(
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
    
    elif model == "NHLTotalBet" and "under_odds" in fields:
        threshold = float(threshold)
        rounded = round(threshold, 1)
        lower_bound = rounded
        upper_bound = rounded + 0.09

        stat_queryset = NHLTotalBet.objects.filter(
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

    elif model == "NHLHandicapBet" and "handicap" in fields:
        match_team_map = {
            match_id: (team1_id, team2_id)
            for match_id, team1_id, team2_id in NHLMatch.objects
                .filter(match_id__in=match_ids)
                .values_list("match_id", "team1_id", "team2_id")
        }

        stat_queryset = NHLHandicapBet.objects.filter(match_id__in=match_ids, period=aggregate)

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
