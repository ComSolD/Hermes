from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime, date
from django.db.models import Q


from .models import NBAMatch, NBAPlayer, NBAPlayerStat, NBATeam, NBATeamStat
from .serializers import NBAHandicapSerializer, NBAMatchSerializer, NBAMatchesSchedule, NBATotalSerializer, NBAMoneylineSerializer, NBATeamStatisticSerializer, NBAPlayerStatisticSerializer, NBAStandingsSerializer  # Импортируем сериализатор матча
from .utils import calculate_statistic_display, handle_statistic_data


@api_view(['GET'])
def match_statistic(request, match_id):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMatchSerializer(match, context={"request": request})

    
    return Response(serializer.data)


@api_view(['GET'])
def match_total(request, match_id, period):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBATotalSerializer(match, context={"period": period, "request": request})

    
    return Response(serializer.data)


@api_view(['GET'])
def match_moneyline(request, match_id):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMoneylineSerializer(match, context={"request": request})

    
    return Response(serializer.data)


@api_view(['GET'])
def match_handicap(request, match_id, period):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAHandicapSerializer(match, context={"period": period, "request": request})

    
    return Response(serializer.data)


@api_view(['GET'])
def schedule(request):
    date_str = request.GET.get("date")  # Получаем дату из запроса


    if not date_str:  # Если даты нет, используем текущий день
        match_date = date.today()
    else:
        try:
            match_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"message": "Неправильный формат даты, используйте YYYY-MM-DD"}, status=400)

    matches = NBAMatch.objects.filter(date=match_date,stage__isnull=False)

    serializer = NBAMatchesSchedule(matches, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def seasons_by_filters(request):
    data = request.data
    filters = Q()

    # Простая мапа: для прямых фильтров
    filter_map = {
        "stage": "stage",
    }

    filters = Q()

    # 1. Простые фильтры
    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    # 2. Особая логика для team_id и opponent_id
    if data.get("team_id"):
        team_id = data["team_id"]
        filters &= Q(team1_id=team_id) | Q(team2_id=team_id)

        if data.get("opponent_id"):
            opponent_id = data["opponent_id"]
            filters &= (
                Q(team1_id=team_id, team2_id=opponent_id) |
                Q(team2_id=team_id, team1_id=opponent_id)
            )

    # 3. Фильтрация матчей
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # 4. Если выбран игрок — ограничиваем по его матчам
    if data.get("player_id"):
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"]
        ).values_list("match_id", flat=True)

        matches = matches.filter(match_id__in=player_match_ids)

    match_ids = matches.values_list("match_id", flat=True)

    teamstat_qs = NBATeamStat.objects.filter(match_id__in=match_ids)

    # 5. Учитываем команду
    if data.get("team_id"):
        teamstat_qs = teamstat_qs.filter(team_id=data["team_id"])

    # 6. Учитываем status (home / away)
    if data.get("homeaway"):
        teamstat_qs = teamstat_qs.filter(status=data["homeaway"])

    # 7. Получаем окончательный список match_id
    filtered_match_ids = teamstat_qs.values_list("match_id", flat=True)

    # 8. Получаем сезоны из NBAMatch
    seasons = NBAMatch.objects.filter(match_id__in=filtered_match_ids).values_list("season", flat=True).distinct()

    return Response({"seasons": list(seasons)})


@api_view(['POST'])
def stages_by_filters(request):
    data = request.data
    filters = Q()

    # Простая мапа: для прямых фильтров
    filter_map = {
        "season": "season",
    }

    filters = Q()

    # 1. Простые фильтры
    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    # 2. Особая логика для team_id и opponent_id
    if data.get("team_id"):
        team_id = data["team_id"]
        filters &= Q(team1_id=team_id) | Q(team2_id=team_id)

        if data.get("opponent_id"):
            opponent_id = data["opponent_id"]
            filters &= (
                Q(team1_id=team_id, team2_id=opponent_id) |
                Q(team2_id=team_id, team1_id=opponent_id)
            )

    # 3. Фильтрация матчей
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # 4. Если выбран игрок — ограничиваем по его матчам
    if data.get("player_id"):
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"]
        ).values_list("match_id", flat=True)

        matches = matches.filter(match_id__in=player_match_ids)

    match_ids = matches.values_list("match_id", flat=True)

    # Промежуточный фильтр NBATeamStat по статусу и (если есть) команде
    teamstat_filters = Q(match_id__in=match_ids)
    if data.get("team_id"):
        teamstat_filters &= Q(team_id=data["team_id"])
    if data.get("homeaway"):
        teamstat_filters &= Q(status=data["homeaway"])

    filtered_match_ids = NBATeamStat.objects.filter(teamstat_filters).values_list("match_id", flat=True)

    # Получение стадий
    raw_stages = NBAMatch.objects.filter(match_id__in=filtered_match_ids).values_list("stage", flat=True).distinct()
    stage_choices_dict = dict(NBAMatch._meta.get_field("stage").choices)

    # 7. Формируем [{ value: 'regular', label: 'Регулярный сезон' }, ...]
    stages = [
        {"value": stage, "label": stage_choices_dict.get(stage, stage)}
        for stage in raw_stages if stage
    ]

    return Response({"stages": list(stages)})


@api_view(['POST'])
def homeaway_by_filters(request):
    data = request.data
    filters = Q()

    # 1. Простая фильтрация матчей (по stage, season, team/opponent/player)
    filter_map = {
        "season": "season",
        "stage": "stage",
    }

    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    # Команда и оппонент
    if data.get("team_id"):
        team_id = data["team_id"]
        filters &= Q(team1_id=team_id) | Q(team2_id=team_id)

        if data.get("opponent_id"):
            opponent_id = data["opponent_id"]
            filters &= (
                Q(team1_id=team_id, team2_id=opponent_id) |
                Q(team2_id=team_id, team1_id=opponent_id)
            )

    # Получаем все подходящие матчи
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # Фильтр по игроку
    if data.get("player_id"):
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"]
        ).values_list("match_id", flat=True)
        matches = matches.filter(match_id__in=player_match_ids)

    match_ids = matches.values_list("match_id", flat=True)

    # 2. Фильтрация по NBATeamStat и получение статусов
    teamstat_qs = NBATeamStat.objects.filter(match_id__in=match_ids)

    if data.get("team_id"):
        teamstat_qs = teamstat_qs.filter(team_id=data["team_id"])

    raw_statuses = teamstat_qs.values_list("status", flat=True).distinct()

    # 3. Форматируем ответ с учетом CHOICES
    status_dict = dict(NBATeamStat.STATUS_CHOICES)

    statuses = [
        { "value": status, "label": status_dict.get(status, status) }
        for status in raw_statuses if status
    ]

    return Response({ "homeaways": statuses })


@api_view(['POST'])
def opponents_by_filters(request):
    data = request.data
    filters = Q()

    # 1. Простые фильтры
    filter_map = {
        "season": "season",
        "stage": "stage",
    }

    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    # 2. Обязательная проверка: выбранная команда
    team_id = data.get("team_id")
    if not team_id:
        return Response({"opponents": []})  # Без команды — нет оппонентов

    # 3. Добавляем условие на участие команды в матчах
    filters &= Q(team1_id=team_id) | Q(team2_id=team_id)

    # 4. Фильтрация матчей
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # 5. Если выбран игрок — фильтруем только матчи с его участием
    if data.get("player_id"):
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"]
        ).values_list("match_id", flat=True)

        matches = matches.filter(match_id__in=player_match_ids)

    match_ids = matches.values_list("match_id", flat=True)

    # 6. Промежуточный фильтр NBATeamStat по status и team_id
    teamstat_filters = Q(match_id__in=match_ids, team_id=team_id)
    if data.get("homeaway"):
        teamstat_filters &= Q(status=data["homeaway"])

    relevant_match_ids = NBATeamStat.objects.filter(teamstat_filters).values_list("match_id", flat=True)

    # 7. Повторный фильтр матчей, чтобы найти оппонентов
    relevant_matches = NBAMatch.objects.filter(match_id__in=relevant_match_ids)

    
    team1_opponents = relevant_matches.filter(team2_id=team_id).values_list("team1_id", flat=True)
    team2_opponents = relevant_matches.filter(team1_id=team_id).values_list("team2_id", flat=True)
    opponent_ids = set(team1_opponents) | set(team2_opponents)

    # 8. Получаем объекты команд
    opponents = NBATeam.objects.filter(team_id__in=opponent_ids)
    serializer = NBATeamStatisticSerializer(opponents, many=True)

    return Response({"opponents": serializer.data})


@api_view(['POST'])
def teams_by_filters(request):
    data = request.data
    filters = Q()

    # 1. Простые фильтры
    filter_map = {
        "season": "season",
        "stage": "stage",
    }

    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    # 2. Фильтрация матчей по фильтрам
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    match_ids = matches.values_list("match_id", flat=True)


    # 3. Получение всех команд
    if data.get("player_id"):
        team_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"],
            match_id__in=matches.values_list("match_id", flat=True)
        ).values_list("team_id", flat=True).distinct()
    else:
        if data.get("homeaway"):
            team_ids = NBATeamStat.objects.filter(
                match_id__in=match_ids,
                status=data["homeaway"]
            ).values_list("team_id", flat=True).distinct()
        else:
            team1_ids = matches.values_list("team1_id", flat=True)
            team2_ids = matches.values_list("team2_id", flat=True)
            team_ids = set(team1_ids) | set(team2_ids)

    teams = NBATeam.objects.filter(team_id__in=team_ids)

    # 4. Сериализация
    serializer = NBATeamStatisticSerializer(teams, many=True)

    return Response({ "teams": serializer.data })


@api_view(['POST'])
def players_by_filters(request):
    data = request.data
    filters = Q()

    # 1. Простые фильтры
    filter_map = {
        "season": "season",
        "stage": "stage",
    }

    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    if data.get("team_id"):
        team_id = data["team_id"]
        filters &= Q(team1_id=data["team_id"]) | Q(team2_id=data["team_id"])

        if data.get("opponent_id"):
            opponent_id = data["opponent_id"]
            filters &= (
                Q(team1_id=team_id, team2_id=opponent_id) |
                Q(team2_id=team_id, team1_id=opponent_id)
            )

    # 2. Находим матчи по фильтрам
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # 3. Получаем ID этих матчей
    match_ids = matches.values_list("match_id", flat=True)

    # 4. Находим игроков, которые играли в этих матчах
    player_stats_filter = Q(match_id__in=match_ids)

    if data.get("team_id"):
        player_stats_filter &= Q(team_id=data["team_id"])


    if data.get("homeaway"):
        # Находим match_id + team_id, соответствующие статусу
        valid_team_stats = NBATeamStat.objects.filter(
            match_id__in=match_ids,
            team_id=data.get("team_id") if data.get("team_id") else None,
            status=data["homeaway"]
        ).values_list("match_id", "team_id")

        # Преобразуем в set для ускорения поиска
        valid_pairs = set(valid_team_stats)

        # Уточняем фильтр: только если match_id и team_id совпадают
        player_ids = NBAPlayerStat.objects.filter(player_stats_filter).filter(
            Q(*[
                Q(match_id=match_id, team_id=team_id)
                for match_id, team_id in valid_pairs
            ], _connector=Q.OR)
        ).values_list("player_id", flat=True).distinct()
    else:
        player_ids = NBAPlayerStat.objects.filter(player_stats_filter).values_list("player_id", flat=True).distinct()


    # 5. Получаем игроков
    players = NBAPlayer.objects.filter(player_id__in=player_ids)

    # 6. Сериализация
    serializer = NBAPlayerStatisticSerializer(players, many=True)

    return Response({"players": serializer.data})


@api_view(['POST'])
def filter_stat(request):
    data = request.data

    filters = Q()

    filter_map = {
        "season": "season",
        "stage": "stage",
    }

    for param, field in filter_map.items():
        value = data.get(param)
        if value:
            filters &= Q(**{field: value})

    if data.get("team_id"):
        team_id = data["team_id"]
        filters &= Q(team1_id=data["team_id"]) | Q(team2_id=data["team_id"])

        if data.get("opponent_id"):
            opponent_id = data["opponent_id"]
            filters &= (
                Q(team1_id=team_id, team2_id=opponent_id) |
                Q(team2_id=team_id, team1_id=opponent_id)
            )

    # 1. Фильтрация матчей
    matches = NBAMatch.objects.filter(filters).exclude(stage__isnull=True)

    # 2. Если выбран игрок — ограничиваем по его матчам
    player_id = data.get("player_id")
    if player_id:
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=player_id
        ).values_list("match_id", flat=True)

        matches = matches.filter(match_id__in=player_match_ids)

    match_ids = list(matches.values_list("match_id", flat=True))

    # Ограничение по положению (home/away)
    valid_match_team_pairs = set()
    status = data.get("homeaway")

    if status and team_id:
        valid_match_team_pairs = set(
            NBATeamStat.objects.filter(
                match_id__in=match_ids,
                team_id=team_id,
                status=status
            ).values_list("match_id", "team_id")
        )
        # 🔸 можно сузить список матчей
        match_ids = [mid for mid, tid in valid_match_team_pairs]
        matches = matches.filter(match_id__in=match_ids)

    match_ids = list(
        matches.order_by("date", "time").values_list("match_id", flat=True)
    )

    # 3. Ограничение по лимиту матчей
    limitation = data.get("limitation")

    if limitation:
        try:
            count, order = limitation.split()
            count = int(count)
            if order.upper() == "ASC":
                matches = matches.order_by("date")[:count]
            else:
                matches = matches.order_by("-date")[:count]
        except Exception:
            pass
    
    # 4. Обработка статистики
    statistic_data = data.get("statistic")
    statistic_values = []

    statistic_values = handle_statistic_data(statistic_data, matches, data, player_id)

    display_mode = data.get("display")

    display_result = calculate_statistic_display(statistic_values, display_mode)

    # Можно добавить реальные поля (победы, очки и т.д.)
    result = {
        "total_matches": matches.count(),
        "example_match_ids": list(matches.values_list("match_id", flat=True)),  # просто пример
        "statistic_display": display_result,
    }
    return Response({
        "answer": result
    })


@api_view(['GET'])
def standings(request):
    season = request.GET.get('season')
    league = request.GET.get('league')

    if not season:
        return Response({"error": "Season is required."}, status=400)

    # Получаем все team_id, участвовавшие в regular или world_tour
    matches = NBAMatch.objects.filter(
        season=season,
        stage__in=["regular", "world tour"]
    ).values_list("team1_id", "team2_id")

    # Собираем уникальные ID команд
    team_ids = set()
    for t1, t2 in matches:
        team_ids.update([t1, t2])

    # Получаем команды, участвующие в этих матчах
    teams = NBATeam.objects.filter(team_id__in=team_ids)
    if league:
        teams = teams.filter(league=league)

    # Сериализация с контекстом
    serializer = NBAStandingsSerializer(teams, many=True, context={"request": request, "season": season})

    # Сортировка по количеству побед
    sorted_data = sorted(serializer.data, key=lambda x: x["wins"], reverse=True)

    return Response({"results": sorted_data})


@api_view(['GET'])
def seasons(request):
    seasons = NBAMatch.objects.values_list("season", flat=True).distinct()
    return Response({"seasons": sorted(seasons, reverse=True)})
