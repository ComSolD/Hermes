from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime, date

from .models import NBAMatch
from .serializers import NBAHandicapSerializer, NBAMatchSerializer, NBAMatchesSchedule, NBATotalSerializer, NBAMoneylineSerializer  # Импортируем сериализатор матча



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


@api_view(['GET'])
def statistic(request):
    print("Im here")

