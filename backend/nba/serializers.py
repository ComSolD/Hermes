from datetime import datetime
from rest_framework import serializers
from django.utils import timezone
from nba.models import NBATeamPtsStat, NBAUpdate, NBAMatch, NBAMoneylineBet, NBATeam

class NBAMatchSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_updated_at(self, obj):
        """Возвращает последнее обновление NBA турнира."""
        last_update = NBAUpdate.objects.last()
        if last_update:
            moscow_time = last_update.updated_at.astimezone(timezone.get_current_timezone())
            return moscow_time.strftime("%d-%m-%Y %H:%M:%S")
        return "Нет обновлений"

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        bet = NBAMoneylineBet.objects.filter(match_id=match.match_id).first()
        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id).first()

        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

        ml_result_team = NBATeam.objects.filter(team_id=bet.ml_result).first() if bet and bet.ml_result else None
        handicap_result_team = NBATeam.objects.filter(team_id=bet.handicap_result).first() if bet and bet.handicap_result else None


        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "away_pts": pts.total if pts else "N/A",
            "home_pts": pts.total_missed if pts else "N/A",
            "ml_result": ml_result_team.name if ml_result_team else "N/A",
            "ml_home": bet.ml_team2_parlay if bet else "N/A",
            "ml_away": bet.ml_team1_parlay if bet else "N/A",
            "ml_parlay": bet.ml_team1_parlay if bet and bet.ml_result == str(bet.team1_id) else bet.ml_team2_parlay if bet else "N/A",
            "total": bet.total if bet else "N/A",
            "total_result": bet.total_result if bet else "N/A",
            "total_parlay": bet.over_total_parlay if bet and bet.total_result == "over" else bet.under_total_parlay if bet else "N/A",
            "total_over": bet.over_total_parlay if bet else "N/A",
            "total_under": bet.under_total_parlay if bet else "N/A",
            "handicap_result": handicap_result_team.name if handicap_result_team else "N/A",
            "handicap": bet.handicap_team1 if bet and bet.handicap_result == str(bet.team1_id) else bet.handicap_team2 if bet else "N/A",
            "handicap_home": bet.handicap_team2 if bet else "N/A",
            "handicap_away": bet.handicap_team1 if bet else "N/A",
            "handicap_home_parlay": bet.handicap_team2_parlay if bet else "N/A",
            "handicap_away_parlay": bet.handicap_team1_parlay if bet else "N/A",
            "handicap_parlay": bet.handicap_team1_parlay if bet and bet.handicap_result == str(bet.team1_id) else bet.handicap_team2_parlay if bet else "N/A",
            "date": match.date.strftime("%d-%m-%Y"),
        }
