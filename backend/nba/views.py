from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache

from .models import NBAMatch
from .serializers import NBAMatchSerializer  # Импортируем сериализатор матча


class HomePage(APIView):

    def get(self, request, *args, **kwargs):
        
        return Response({"message": "Гермес - путеводитель по статистике!"})



@api_view(['GET'])
def match(request, match_id):

    # print(match_id)

    # match = NBAMatch.objects.filter(match_id=match_id).first()


    match = get_object_or_404(NBAMatch, match_id=match_id)

    # Сериализуем данные
    serializer = NBAMatchSerializer(match)

    
    return Response(serializer.data)

    
