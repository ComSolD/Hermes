from rest_framework import serializers
from .models import NBAMatch  # Импортируем модель

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBAMatch
        fields = '__all__'  # Или перечисли конкретные поля
