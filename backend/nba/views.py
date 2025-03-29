from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime, date
from django.db.models import Q, Sum

from .models import NBAMatch, NBAPlayer, NBAPlayerStat, NBATeam, NBATeamPtsStat
from .serializers import NBAHandicapSerializer, NBAMatchSerializer, NBAMatchesSchedule, NBATotalSerializer, NBAMoneylineSerializer, NBATeamStatisticSerializer, NBAPlayerStatisticSerializer  # Импортируем сериализатор матча
from .utils import calculate_statistic_display


@api_view(['GET'])
def match_statistic(request, match_id):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMatchSerializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_total(request, match_id, period):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBATotalSerializer(match, context={"period": period})

    
    return Response(serializer.data)


@api_view(['GET'])
def match_moneyline(request, match_id):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMoneylineSerializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_handicap(request, match_id, period):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAHandicapSerializer(match, context={"period": period})

    
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

    # 5. Получение сезонов
    seasons = matches.values_list("season", flat=True).distinct()

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

    # 5. Получение стадий
    raw_stages = matches.values_list("stage", flat=True).distinct()

    # 6. Получаем список всех choices из модели
    stage_choices_dict = dict(NBAMatch._meta.get_field("stage").choices)

    # 7. Формируем [{ value: 'regular', label: 'Регулярный сезон' }, ...]
    stages = [
        {"value": stage, "label": stage_choices_dict.get(stage, stage)}
        for stage in raw_stages if stage
    ]

    return Response({"stages": list(stages)})


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

    # 6. Находим соперников
    team1_opponents = matches.filter(team2_id=team_id).values_list("team1_id", flat=True)
    team2_opponents = matches.filter(team1_id=team_id).values_list("team2_id", flat=True)
    opponent_ids = set(team1_opponents) | set(team2_opponents)

    # 7. Получаем объекты команд
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

    # 3. Получение всех команд
    if data.get("player_id"):
        team_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"],
            match_id__in=matches.values_list("match_id", flat=True)
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
    if data.get("player_id"):
        player_match_ids = NBAPlayerStat.objects.filter(
            player_id=data["player_id"]
        ).values_list("match_id", flat=True)

        matches = matches.filter(match_id__in=player_match_ids)

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

    if statistic_data and isinstance(statistic_data, dict):
        model = statistic_data.get("model")
        fields = statistic_data.get("fields", [])

        match_ids = list(matches.values_list("match_id", flat=True))
        team_id = data.get("team_id")

        match_stat_map = {mid: 0 for mid in match_ids}

        if model == "NBATeamPtsStat":
            stat_queryset = NBATeamPtsStat.objects.filter(match_id__in=match_ids)

            for stat in stat_queryset:
                if str(stat.team_id) != team_id:
                    continue  # учитываем только выбранную команду
                total = sum([getattr(stat, f, 0) or 0 for f in fields])
                match_stat_map[stat.match_id] += total

        # В будущем: elif model == "NBAPlayerStat": ...

        statistic_values = [match_stat_map[mid] for mid in match_ids if mid in match_stat_map]

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
    