from django.db.models import Q, Case, IntegerField, Max, When
from django.utils import timezone
from rest_framework import serializers

from nba.models import NBATeamPtsStat, NBAUpdate, NBAMatch, NBAMoneylineBet, NBATeam
from nfl.models import NFLTeamPtsStat, NFLUpdate, NFLMatch, NFLBet, NFLTeam
from nhl.models import NHLTeamPtsStat, NHLUpdate, NHLMatch, NHLBet, NHLTeam

from .models import Tournament

UPDATE_MODELS = {
    "NBA": NBAUpdate,
    "NHL": NHLUpdate,
    "NFL": NFLUpdate,
}

MATCH_MODELS = {
    "NBA": (NBAMatch, NBAMoneylineBet, NBATeam, NBATeamPtsStat),
    "NHL": (NHLMatch, NHLBet, NHLTeam, NHLTeamPtsStat),
    "NFL": (NFLMatch, NFLBet, NFLTeam, NFLTeamPtsStat),
}

class TournamentSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()  # Добавляем поле с временем обновления
    upcoming_matches = serializers.SerializerMethodField()  # Будущие матчи
    past_matches = serializers.SerializerMethodField()  # Прошедшие матчи

    class Meta:
        model = Tournament
        fields = ['name', 'updated_at', 'upcoming_matches', 'past_matches']

    def get_updated_at(self, obj):
        # Проверяем, к какому турниру относится запись, и берём последнее обновление
        UpdateModel = UPDATE_MODELS.get(obj.name)

        if UpdateModel:
            last_update = UpdateModel.objects.last()
            moscow_time = last_update.updated_at.astimezone(timezone.get_current_timezone())
            return moscow_time.strftime("%d-%m-%Y %H:%M:%S") if last_update else "Нет обновлений"
        return "Нет обновлений"

    def get_matches(self, obj, is_upcoming=True):
        MatchModel, BetModel, TeamModel, PTSModel = MATCH_MODELS.get(obj.name, (None, None, None, None))
        if not MatchModel or not BetModel or not TeamModel or not PTSModel:
            return []

        if obj.name == "NFL":
            if is_upcoming:
                matches = MatchModel.objects.filter(
                    match_id__in=BetModel.objects.filter(ml_result__isnull=True).values('match_id')
                ).order_by('stage')  # Сортируем по stage для грядущих матчей
            else:


                last_week = MatchModel.objects.filter(
                    match_id__in=BetModel.objects.filter(ml_result__isnull=False).values('match_id')
                ).order_by('-season_type', '-week').values('season_type', 'week').first()

                matches = MatchModel.objects.filter(
                    match_id__in=BetModel.objects.filter(ml_result__isnull=False).values('match_id'),
                    season_type=last_week['season_type'],
                    week=last_week['week'],
                )
                
        else:
            # Для других турниров используем date
            if is_upcoming:
                matches = MatchModel.objects.filter(
                    match_id__in=BetModel.objects.filter(ml_result__isnull=True).values('match_id')
                ).order_by('date')
            else:
                last_date = MatchModel.objects.filter(
                match_id__in=BetModel.objects.filter(ml_result__isnull=False).values('match_id')
                ).order_by('-date').values_list('date', flat=True).first()

                matches = MatchModel.objects.filter(
                    match_id__in=BetModel.objects.filter(ml_result__isnull=False).values('match_id'),
                    date=last_date  # Фильтруем только по этой дате
                )

        # Форматируем список матчей
        result = []

        for match in matches:
            bet = BetModel.objects.filter(match_id=match.match_id).first()

            pts = PTSModel.objects.filter(match_id=match.match_id).first()

            # Переводим `team_id` в `name`
            home_team = TeamModel.objects.filter(team_id=match.team2_id).first()
            away_team = TeamModel.objects.filter(team_id=match.team1_id).first()

            ml_result = TeamModel.objects.filter(team_id=bet.ml_result).first() 
            spread_result = TeamModel.objects.filter(team_id=bet.spread_result).first()

            match_info = {
                "match_id": match.match_id,
                "home_team": home_team.name if home_team else "Unknown",
                "away_team": away_team.name if away_team else "Unknown",
                "away_pts": pts.total if pts else "Unknown",
                "home_pts": pts.total_missed if pts else "Unknown",
                "match_bet": {
                    "total": bet.total if bet.total else "N/A",
                    "total_result": bet.total_result if bet.total_result else "N/A",
                    "total_parlay": bet.over_total_parlay if bet.total_result == "over" else bet.under_total_parlay,
                    "total_over": bet.over_total_parlay if bet.over_total_parlay else "N/A",
                    "total_under": bet.under_total_parlay if bet.under_total_parlay else "N/A",
                    "ml_result": ml_result.name if bet.ml_result else "N/A",
                    "ml_home": bet.ml_team2_parlay if bet.ml_team2_parlay else "N/A",
                    "ml_away": bet.ml_team1_parlay if bet.ml_team1_parlay else "N/A",
                    "ml_parlay": bet.ml_team1_parlay if bet.ml_result == str(bet.team1_id) else bet.ml_team2_parlay,
                    "spread_result": spread_result.name if bet.spread_result else "N/A",
                    "spread": bet.spread_team1 if bet.spread_result == str(bet.team1_id) else bet.spread_team2,
                    "spread_home": bet.spread_team2 if bet.spread_team2 else "N/A",
                    "spread_away": bet.spread_team1 if bet.spread_team1 else "N/A",
                    "spread_home_parlay": bet.spread_team2_parlay if bet.spread_team2_parlay else "N/A",
                    "spread_away_parlay": bet.spread_team1_parlay if bet.spread_team1_parlay else "N/A",
                    "spread_parlay": bet.spread_team1_parlay if bet.spread_result == str(bet.team1_id) else bet.spread_team2_parlay,
                }
            }

            if obj.name == "NFL":
                match_info["stage"] = match.stage  # Используем stage для NFL
            else:
                match_info["date"] = match.date.strftime("%d-%m-%Y")

            result.append(match_info)

        return result

    def get_upcoming_matches(self, obj):
        return self.get_matches(obj, is_upcoming=True)

    def get_past_matches(self, obj):
        return self.get_matches(obj, is_upcoming=False)
