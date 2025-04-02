from django.db.models import Q, Case, IntegerField, Max, When
from django.utils import timezone
from rest_framework import serializers

from nba.models import NBATeamPtsStat, NBAUpdate, NBAMatch, NBAMoneylineBet, NBATeam
from mlb.models import MLBTeamPtsStat, MLBUpdate, MLBMatch, MLBMoneylineBet, MLBTeam

from nhl.models import NHLTeamPtsStat, NHLUpdate, NHLMatch, NHLMoneylineBet, NHLTeam

from .models import Tournament

UPDATE_MODELS = {
    "NBA": NBAUpdate,
    "MLB": MLBUpdate,



    "NHL": NHLUpdate,
}

MATCH_MODELS = {
    "NBA": (NBAMatch, NBAMoneylineBet, NBATeam, NBATeamPtsStat),
    "MLB": (MLBMatch, MLBMoneylineBet, MLBTeam, MLBTeamPtsStat),


    "NHL": (NHLMatch, NHLMoneylineBet, NHLTeam, NHLTeamPtsStat),

}

class TournamentSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()  # Добавляем поле с временем обновления
    past_matches = serializers.SerializerMethodField()  # Прошедшие матчи

    class Meta:
        model = Tournament
        fields = ['name', 'updated_at', 'past_matches']

    def get_updated_at(self, obj):
        # Проверяем, к какому турниру относится запись, и берём последнее обновление
        UpdateModel = UPDATE_MODELS.get(obj.name)

        if UpdateModel:
            last_update = UpdateModel.objects.last()
            moscow_time = last_update.updated_at.astimezone(timezone.get_current_timezone())
            return moscow_time.strftime("%d-%m-%Y %H:%M:%S") if last_update else "Нет обновлений"
        return "Нет обновлений"

    def get_matches(self, obj):
        MatchModel, BetModel, TeamModel, PTSModel = MATCH_MODELS.get(obj.name, (None, None, None, None))
        if not MatchModel or not BetModel or not TeamModel or not PTSModel:
            return []

        if obj.name == "NFL":


            last_week = MatchModel.objects.filter(
                match_id__in=BetModel.objects.filter(result__isnull=False).values('match_id')
            ).order_by('-season_type', '-week').values('season_type', 'week').first()

            matches = MatchModel.objects.filter(
                match_id__in=BetModel.objects.filter(result__isnull=False).values('match_id'),
                season_type=last_week['season_type'],
                week=last_week['week'],
                )
                
        else:
            # Для других турниров используем date

            last_date = MatchModel.objects.filter(
            match_id__in=BetModel.objects.filter(result__isnull=False).values('match_id')
            ).order_by('-date').values_list('date', flat=True).first()

            matches = MatchModel.objects.filter(
                match_id__in=BetModel.objects.filter(result__isnull=False).values('match_id'),
                date=last_date  # Фильтруем только по этой дате
            )

        # Форматируем список матчей
        result = []

        for match in matches:
            bet = BetModel.objects.filter(match_id=match.match_id, period='full_time').first()

            pts = PTSModel.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

            # Переводим `team_id` в `name`
            home_team = TeamModel.objects.filter(team_id=match.team2_id).first()
            away_team = TeamModel.objects.filter(team_id=match.team1_id).first()

            ml_result = TeamModel.objects.filter(team_id=bet.result).first()

            match_info = {
                "match_id": match.match_id,
                "home_team": home_team.name if home_team else "Unknown",
                "away_team": away_team.name if away_team else "Unknown",
                "away_pts": pts.total if pts else "Unknown",
                "home_pts": pts.total_missed if pts else "Unknown",
                "match_bet": {
                    "ml_result": ml_result.name if bet.result else "N/A",
                    "ml_odds": bet.team2_odds if bet.result == str(match.team2_id) else bet.team1_odds,
                },
                "time": match.time.strftime("%H:%M"),
            }

           
            if obj.name == "NFL":
                match_info["stage"] = match.stage  # Используем stage для NFL
            else:
                match_info["date"] = match.date.strftime("%d-%m-%Y")

            result.append(match_info)

        return result

    def get_past_matches(self, obj):
        return self.get_matches(obj)
