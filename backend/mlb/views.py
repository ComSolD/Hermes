from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache

from .models import MLBMatch
# from .serializers import MLBMatchSerializer  # Импортируем сериализатор матча



@api_view(['GET'])
def match(request, match_id):

    print(match_id)

    # match = MLBMatch.objects.filter(match_id=match_id).first()


    # match = get_object_or_404(MLBMatch, match_id=match_id)

    # # Сериализуем данные
    # serializer = MLBMatchSerializer(match)

    
    # return Response(serializer.data)

    
