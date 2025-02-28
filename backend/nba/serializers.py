from datetime import datetime
from rest_framework import serializers
from django.utils import timezone
from nba.models import NBAPlayer, NBAPlayerStat, NBATeamPtsStat, NBATeamStat, NBAUpdate, NBAMatch, NBAMoneylineBet, NBATeam

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
        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        ml_result_team = NBATeam.objects.filter(team_id=bet.result).first() if bet and bet.result else None

        # Домашняя команда
        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()

        home_stat = NBATeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

            # Стартер
        home_starter_players = NBAPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="starter")

        home_starter_players_info = [{"player": NBAPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "pts": p.pts,
            "fg": p.fg,
            "trying_fg": p.trying_fg,
            "three_pt": p.three_pt,
            "attempted_three_pt": p.attempted_three_pt,
            "ft": p.ft,
            "trying_ft": p.trying_ft,
            "oreb": p.oreb,
            "dreb": p.dreb,
            "reb": p.reb,
            "ast": p.ast,
            "stl": p.stl,
            "blk": p.blk,
            "turnovers": p.turnovers,
            "pf": p.pf,
            "plus_minus": p.plus_minus,
            "min": p.min,
        } for p in home_starter_players]

            # Скамейка
        home_bench_players = NBAPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="bench")

        home_bench_players_info = [{"player": NBAPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "pts": p.pts,
            "fg": p.fg,
            "trying_fg": p.trying_fg,
            "three_pt": p.three_pt,
            "attempted_three_pt": p.attempted_three_pt,
            "ft": p.ft,
            "trying_ft": p.trying_ft,
            "oreb": p.oreb,
            "dreb": p.dreb,
            "reb": p.reb,
            "ast": p.ast,
            "stl": p.stl,
            "blk": p.blk,
            "turnovers": p.turnovers,
            "pf": p.pf,
            "plus_minus": p.plus_minus,
            "min": p.min,
        } for p in home_bench_players]

        # Выездная команда
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

        away_stat = NBATeamStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

            # Стартер
        away_starter_players = NBAPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="starter")

        away_starter_players_info = [{"player": NBAPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "pts": p.pts,
            "fg": p.fg,
            "trying_fg": p.trying_fg,
            "three_pt": p.three_pt,
            "attempted_three_pt": p.attempted_three_pt,
            "ft": p.ft,
            "trying_ft": p.trying_ft,
            "oreb": p.oreb,
            "dreb": p.dreb,
            "reb": p.reb,
            "ast": p.ast,
            "stl": p.stl,
            "blk": p.blk,
            "turnovers": p.turnovers,
            "pf": p.pf,
            "plus_minus": p.plus_minus,
            "min": p.min,
        } for p in away_starter_players]


            # Скамейка
        away_bench_players = NBAPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="bench")

        away_bench_players_info = [{"player": NBAPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "pts": p.pts,
            "fg": p.fg,
            "trying_fg": p.trying_fg,
            "three_pt": p.three_pt,
            "attempted_three_pt": p.attempted_three_pt,
            "ft": p.ft,
            "trying_ft": p.trying_ft,
            "oreb": p.oreb,
            "dreb": p.dreb,
            "reb": p.reb,
            "ast": p.ast,
            "stl": p.stl,
            "blk": p.blk,
            "turnovers": p.turnovers,
            "pf": p.pf,
            "plus_minus": p.plus_minus,
            "min": p.min,
        } for p in away_bench_players]


        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_q1": pts.total_q1 if pts else "N/A",
                "away_q2": pts.total_q2 if pts else "N/A",
                "away_q3": pts.total_q3 if pts else "N/A",
                "away_q4": pts.total_q4 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_q1": pts.total_q1_missed if pts else "N/A",
                "home_q2": pts.total_q2_missed if pts else "N/A",
                "home_q3": pts.total_q3_missed if pts else "N/A",
                "home_q4": pts.total_q4_missed if pts else "N/A",
            },

            "home_starter_players": home_starter_players_info,
            "home_bench_players": home_bench_players_info,
            "home_stat": {
                "fg": home_stat.fg,
                "trying_fg": home_stat.trying_fg,
                "three_pt": home_stat.three_pt,
                "attempted_three_pt": home_stat.attempted_three_pt,
                "ft": home_stat.ft,
                "trying_ft": home_stat.trying_ft,
                "oreb": home_stat.oreb,
                "dreb": home_stat.dreb,
                "reb": home_stat.reb,
                "ast": home_stat.ast,
                "stl": home_stat.stl,
                "blk": home_stat.blk,
                "turnovers": home_stat.turnovers,
                "pf": home_stat.pf,
            },

            "away_starter_players": away_starter_players_info,
            "away_bench_players": away_bench_players_info,
            "away_stat": {
                "fg": away_stat.fg,
                "trying_fg": away_stat.trying_fg,
                "three_pt": away_stat.three_pt,
                "attempted_three_pt": away_stat.attempted_three_pt,
                "ft": away_stat.ft,
                "trying_ft": away_stat.trying_ft,
                "oreb": away_stat.oreb,
                "dreb": away_stat.dreb,
                "reb": away_stat.reb,
                "ast": away_stat.ast,
                "stl": away_stat.stl,
                "blk": away_stat.blk,
                "turnovers": away_stat.turnovers,
                "pf": away_stat.pf,
            },


            "ml_result": ml_result_team.name if ml_result_team else "N/A",
            "date": match.date.strftime("%d-%m-%Y"),
        }
