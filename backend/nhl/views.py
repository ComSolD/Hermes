from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime, date

from .models import NHLMatch, NHLTeam
from .serializers import NHLMatchSerializer, NHLTotalSerializer, NHLMoneylineSerializer, NHL1x2Serializer, NHLHandicapSerializer, NHLMatchesSchedule # Импортируем сериализатор матча


@api_view(['GET'])
def match_statistic(request, match_id):


    match = get_object_or_404(NHLMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NHLMatchSerializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_total(request, match_id, period):


    match = get_object_or_404(NHLMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NHLTotalSerializer(match, context={"period": period})

    
    return Response(serializer.data)


@api_view(['GET'])
def match_moneyline(request, match_id):


    match = get_object_or_404(NHLMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NHLMoneylineSerializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_1x2(request, match_id):


    match = get_object_or_404(NHLMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NHL1x2Serializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_handicap(request, match_id, period):


    match = get_object_or_404(NHLMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NHLHandicapSerializer(match, context={"period": period})

    
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

    matches = NHLMatch.objects.filter(date=match_date,stage__isnull=False)

    serializer = NHLMatchesSchedule(matches, many=True)

    return Response(serializer.data)
