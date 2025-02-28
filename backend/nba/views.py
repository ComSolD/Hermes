from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache

from .models import NBAMatch
from .serializers import NBAMatchSerializer, NBATotalSerializer  # Импортируем сериализатор матча



@api_view(['GET'])
def match_statistic(request, match_id):


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMatchSerializer(match)

    
    return Response(serializer.data)


@api_view(['GET'])
def match_total(request, match_id):



    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBATotalSerializer(match)

    
    return Response(serializer.data)

    
