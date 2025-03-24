from rest_framework import serializers
from nba.models import NBAHandicapBet, NBAPlayer, NBAPlayerStat, NBATeamPtsStat, NBATeamStat, NBAMatch, NBAMoneylineBet, NBATeam, NBATotalBet

class NBAMatchSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

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
                "fg": sum(player["fg"] for player in home_starter_players_info) + sum(player["fg"] for player in home_bench_players_info),
                "trying_fg": sum(player["trying_fg"] for player in home_starter_players_info) + sum(player["trying_fg"] for player in home_bench_players_info),
                "three_pt": sum(player["three_pt"] for player in home_starter_players_info) + sum(player["three_pt"] for player in home_bench_players_info),
                "attempted_three_pt": sum(player["attempted_three_pt"] for player in home_starter_players_info) + sum(player["attempted_three_pt"] for player in home_bench_players_info),
                "ft": sum(player["ft"] for player in home_starter_players_info) + sum(player["ft"] for player in home_bench_players_info),
                "trying_ft": sum(player["trying_ft"] for player in home_starter_players_info) + sum(player["trying_ft"] for player in home_bench_players_info),
                "oreb": sum(player["oreb"] for player in home_starter_players_info) + sum(player["oreb"] for player in home_bench_players_info),
                "dreb": sum(player["dreb"] for player in home_starter_players_info) + sum(player["dreb"] for player in home_bench_players_info),
                "reb": sum(player["reb"] for player in home_starter_players_info) + sum(player["reb"] for player in home_bench_players_info),
                "ast": sum(player["ast"] for player in home_starter_players_info) + sum(player["ast"] for player in home_bench_players_info),
                "stl": sum(player["stl"] for player in home_starter_players_info) + sum(player["stl"] for player in home_bench_players_info),
                "blk": sum(player["blk"] for player in home_starter_players_info) + sum(player["blk"] for player in home_bench_players_info),
                "turnovers": sum(player["turnovers"] for player in home_starter_players_info) + sum(player["turnovers"] for player in home_bench_players_info),
                "pf": sum(player["pf"] for player in home_starter_players_info) + sum(player["pf"] for player in home_bench_players_info),
            },

            "away_starter_players": away_starter_players_info,
            "away_bench_players": away_bench_players_info,
            "away_stat": {
                "fg": sum(player["fg"] for player in away_starter_players_info) + sum(player["fg"] for player in away_bench_players_info),
                "trying_fg": sum(player["trying_fg"] for player in away_starter_players_info) + sum(player["trying_fg"] for player in away_bench_players_info),
                "three_pt": sum(player["three_pt"] for player in away_starter_players_info) + sum(player["three_pt"] for player in away_bench_players_info),
                "attempted_three_pt": sum(player["attempted_three_pt"] for player in away_starter_players_info) + sum(player["attempted_three_pt"] for player in away_bench_players_info),
                "ft": sum(player["ft"] for player in away_starter_players_info) + sum(player["ft"] for player in away_bench_players_info),
                "trying_ft": sum(player["trying_ft"] for player in away_starter_players_info) + sum(player["trying_ft"] for player in away_bench_players_info),
                "oreb": sum(player["oreb"] for player in away_starter_players_info) + sum(player["oreb"] for player in away_bench_players_info),
                "dreb": sum(player["dreb"] for player in away_starter_players_info) + sum(player["dreb"] for player in away_bench_players_info),
                "reb": sum(player["reb"] for player in away_starter_players_info) + sum(player["reb"] for player in away_bench_players_info),
                "ast": sum(player["ast"] for player in away_starter_players_info) + sum(player["ast"] for player in away_bench_players_info),
                "stl": sum(player["stl"] for player in away_starter_players_info) + sum(player["stl"] for player in away_bench_players_info),
                "blk": sum(player["blk"] for player in away_starter_players_info) + sum(player["blk"] for player in away_bench_players_info),
                "turnovers": sum(player["turnovers"] for player in away_starter_players_info) + sum(player["turnovers"] for player in away_bench_players_info),
                "pf": sum(player["pf"] for player in away_starter_players_info) + sum(player["pf"] for player in away_bench_players_info),
            },

            "date": match.date.strftime("%d-%m-%Y"),
        }
    

class NBATotalSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор

        period = self.context.get("period")

        period = NBATotalBet._meta.get_field('period').choices

        period_value = NBATotalBet._meta.get_field('period').choices[self.context.get("period")][0]

        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-я Четверть': 2,
            '2-я Четверть': 3,
            '2-я Половина': 4,
            '3-я Четверть': 5,
            '4-я Четверть': 6,
        }

        period = NBATotalBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(NBATotalBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(NBATotalBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        total_odds = NBATotalBet.objects.filter(match_id=match.match_id, period=period_value)

        total_odds_info = [{ "total": to.total,
            "over_odds": to.over_odds,
            "under_odds": to.under_odds,
            "total_result": to.total_result,
            "period": self.context.get("period"),
        } for to in total_odds]

        total_odds_info = sorted(total_odds_info, key=lambda x: x["total"])


        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        # Домашняя команда
        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

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

            "periods": periods,
            "total_odds": total_odds_info,

            "date": match.date.strftime("%d-%m-%Y"),
        }
    

class NBAMoneylineSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-я Четверть': 2,
            '2-я Четверть': 3,
            '2-я Половина': 4,
            '3-я Четверть': 5,
            '4-я Четверть': 6,
        }

        moneyline = NBAMoneylineBet.objects.filter(match_id=match.match_id)
        moneyline_info = [{ "period": ml.get_period_display(),
            "home_odds": ml.team2_odds,
            "away_odds": ml.team1_odds,
        } for ml in moneyline]

        moneyline_info = sorted(moneyline_info, key=lambda x: order_map[x['period']])

        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        # Домашняя команда
        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

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

            "moneyline_info": moneyline_info,

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NBAHandicapSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        period = self.context.get("period")

        period = NBAHandicapBet._meta.get_field('period').choices

        period_value = NBAHandicapBet._meta.get_field('period').choices[self.context.get("period")][0]


        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-я Четверть': 2,
            '2-я Четверть': 3,
            '2-я Половина': 4,
            '3-я Четверть': 5,
            '4-я Четверть': 6,
        }

        period = NBAHandicapBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(NBAHandicapBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(NBAHandicapBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        handicap_odds = NBAHandicapBet.objects.filter(match_id=match.match_id, period=period_value)

        handicap_odds_info = [{ "handicap": h.handicap,
            "handicap_team1_odds": h.handicap_team1_odds,
            "handicap_team2_odds": h.handicap_team2_odds,
            "handicap_team1_result": h.handicap_team1_result,
            "handicap_team2_result": h.handicap_team2_result,
            "period": self.context.get("period"),
        } for h in handicap_odds]

        handicap_odds_info = sorted(handicap_odds_info, key=lambda x: x["handicap"])


        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        # Домашняя команда
        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

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

            "periods": periods,
            "handicap_odds": handicap_odds_info,

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NBAMatchesSchedule(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NBAMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор


        pts = NBATeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        # Домашняя команда
        home_team = NBATeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NBATeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
            },
        }


class NBAStatistic(serializers.ModelSerializer):

    class Meta:
        model = NBATeam
        fields = ['team_id', 'name']
