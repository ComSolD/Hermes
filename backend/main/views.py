from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tournament
from .serializers import TournamentSerializer

@api_view(['GET'])
def home(request):
    tournaments = Tournament.objects.filter(is_active=True)[:3]  # Берём 3 активных турнира
    serializer = TournamentSerializer(tournaments, many=True)
    return Response(serializer.data)

