from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tournament
from .serializers import TournamentSerializer
from django.core.cache import cache

@api_view(['GET'])
def home(request):

    cache_key = "active_tournaments"  # Уникальный ключ кеша
    cached_data = cache.get(cache_key)  # Проверяем кеш


    if cached_data:  # Если кеш есть, отдаем его
        return Response(cached_data)


    tournaments = Tournament.objects.filter(is_active=True)[:3]  # Берём 3 активных турнира
    serializer = TournamentSerializer(tournaments, many=True)

    cache.set(cache_key, serializer.data, timeout=60)

    return Response(serializer.data)

