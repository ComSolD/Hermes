from rest_framework import serializers
from mlb.models import MLBHandicapBet, MLBPlayer, MLBPlayerStat, MLBTeamPtsStat, MLBTeamStat, MLBMatch, MLBMoneylineBet, MLBTeam, MLBTotalBet
from django.db.models import Q


class MLBMatchSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = MLBMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        pts = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        home_error = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        # Домашняя команда
        home_team = MLBTeam.objects.filter(team_id=match.team2_id).first()

            # Бьющий
        home_hitter_players = MLBPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="hitter")

        home_hitter_players_info = [{"player": MLBPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "ab": p.ab,
            "r": p.r,
            "h": p.h,
            "rbi": p.rbi,
            "hr": p.hr,
            "bb": p.bb,
            "k": p.k,
            "avg": p.avg,
            "obp": p.obp,
            "slg": p.slg,
        } for p in home_hitter_players]
        

            # Подающий
        home_pitcher_players = MLBPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="pitcher")

        home_pitcher_players_info = [{"player": MLBPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "ip": p.ip,
            "h": p.h,
            "r": p.r,
            "er": p.er,
            "bb": p.bb,
            "k": p.k,
            "hr": p.hr,
            "pc": p.pc,
            "st": p.st,
            "era": p.era,
        } for p in home_pitcher_players]

        # Выездная команда
        away_team = MLBTeam.objects.filter(team_id=match.team1_id).first()

            # Бьющий
        away_hitter_players = MLBPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="hitter")

        away_hitter_players_info = [{"player": MLBPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "ab": p.ab,
            "r": p.r,
            "h": p.h,
            "rbi": p.rbi,
            "hr": p.hr,
            "bb": p.bb,
            "k": p.k,
            "avg": p.avg,
            "obp": p.obp,
            "slg": p.slg,
        } for p in away_hitter_players]


            # Подающий
        away_pitcher_players = MLBPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="pitcher")

        away_pitcher_players_info = [{"player": MLBPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "ip": p.ip,
            "h": p.h,
            "r": p.r,
            "er": p.er,
            "bb": p.bb,
            "k": p.k,
            "hr": p.hr,
            "pc": p.pc,
            "st": p.st,
            "era": p.era,
        } for p in away_pitcher_players]

        ot = (pts.total_i1 + pts.total_i2 + pts.total_i3 + pts.total_i4 + pts.total_i5 + pts.total_i6 + pts.total_i7 + pts.total_i8 + pts.total_i9 + pts.total_i1_missed + pts.total_i2_missed + pts.total_i3_missed + pts.total_i4_missed + pts.total_i5_missed + pts.total_i6_missed + pts.total_i7_missed + pts.total_i8_missed + pts.total_i9_missed) - (pts.total + pts.total_missed)

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_hit": pts.hit if pts else "N/A",
                "away_error": pts.error if pts else "N/A",
                "away_i1": pts.total_i1 if pts else "N/A",
                "away_i2": pts.total_i2 if pts else "N/A",
                "away_i3": pts.total_i3 if pts else "N/A",
                "away_i4": pts.total_i4 if pts else "N/A",
                "away_i5": pts.total_i5 if pts else "N/A",
                "away_i6": pts.total_i6 if pts else "N/A",
                "away_i7": pts.total_i7 if pts else "N/A",
                "away_i8": pts.total_i8 if pts else "N/A",
                "away_i9": pts.total_i9 if pts else "N/A",

                "home_total": pts.total_missed if pts else "N/A",
                "home_hit": pts.hit_missed if pts else "N/A",
                "home_error": home_error.error if home_error else "N/A",
                "home_i1": pts.total_i1_missed if pts else "N/A",
                "home_i2": pts.total_i2_missed if pts else "N/A",
                "home_i3": pts.total_i3_missed if pts else "N/A",
                "home_i4": pts.total_i4_missed if pts else "N/A",
                "home_i5": pts.total_i5_missed if pts else "N/A",
                "home_i6": pts.total_i6_missed if pts else "N/A",
                "home_i7": pts.total_i7_missed if pts else "N/A",
                "home_i8": pts.total_i8_missed if pts else "N/A",
                "home_i9": pts.total_i9_missed if pts else "N/A",

            },

            "home_hitter_players": home_hitter_players_info,
            "home_pitcher_players": home_pitcher_players_info,
            "home_stat_hitter": {
                "ab": sum(player["ab"] for player in home_hitter_players_info),
                "r": sum(player["r"] for player in home_hitter_players_info),
                "h": sum(player["h"] for player in home_hitter_players_info),
                "rbi": sum(player["rbi"] for player in home_hitter_players_info),
                "hr": sum(player["hr"] for player in home_hitter_players_info),
                "bb": sum(player["bb"] for player in home_hitter_players_info),
                "k": sum(player["k"] for player in home_hitter_players_info),
            },
            "home_stat_pitcher": {
                "ip": sum(player["ip"] for player in home_pitcher_players_info),
                "h": sum(player["h"] for player in home_pitcher_players_info),
                "r": sum(player["r"] for player in home_pitcher_players_info),
                "er": sum(player["er"] for player in home_pitcher_players_info),
                "bb": sum(player["bb"] for player in home_pitcher_players_info),
                "k": sum(player["k"] for player in home_pitcher_players_info),
                "hr": sum(player["hr"] for player in home_pitcher_players_info),
                "pc": sum(player["pc"] for player in home_pitcher_players_info),
                "st": sum(player["st"] for player in home_pitcher_players_info),
            },

            "away_hitter_players": away_hitter_players_info,
            "away_pitcher_players": away_pitcher_players_info,
            "away_stat_hitter": {
                "ab": sum(player["ab"] for player in away_hitter_players_info),
                "r": sum(player["r"] for player in away_hitter_players_info),
                "h": sum(player["h"] for player in away_hitter_players_info),
                "rbi": sum(player["rbi"] for player in away_hitter_players_info),
                "hr": sum(player["hr"] for player in away_hitter_players_info),
                "bb": sum(player["bb"] for player in away_hitter_players_info),
                "k": sum(player["k"] for player in away_hitter_players_info),
            },
            "away_stat_pitcher": {
                "ip": sum(player["ip"] for player in away_pitcher_players_info),
                "h": sum(player["h"] for player in away_pitcher_players_info),
                "r": sum(player["r"] for player in away_pitcher_players_info),
                "er": sum(player["er"] for player in away_pitcher_players_info),
                "bb": sum(player["bb"] for player in away_pitcher_players_info),
                "k": sum(player["k"] for player in away_pitcher_players_info),
                "hr": sum(player["hr"] for player in away_pitcher_players_info),
                "pc": sum(player["pc"] for player in away_pitcher_players_info),
                "st": sum(player["st"] for player in away_pitcher_players_info),
            },

            "ot": ot,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class MLBTotalSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = MLBMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        period = self.context.get("period")

        period = MLBTotalBet._meta.get_field('period').choices

        period_value = MLBTotalBet._meta.get_field('period').choices[self.context.get("period")][0]

        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-й Иннинг': 2,
            '2-й Иннинг': 3,
            '3-й Иннинг': 4,
            '4-й Иннинг': 5,
            '5-й Иннинг': 6,
            '2-я Половина': 7,
            '6-й Иннинг': 8,
            '7-й Иннинг': 9,
            '8-й Иннинг': 10,
            '9-й Иннинг': 11,
        }

        period = MLBTotalBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(MLBTotalBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(MLBTotalBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        total_odds = MLBTotalBet.objects.filter(match_id=match.match_id, period=period_value)

        total_odds_info = [{ "total": to.total,
            "over_odds": to.over_odds,
            "under_odds": to.under_odds,
            "total_result": to.total_result,
            "period": self.context.get("period"),
        } for to in total_odds]

        total_odds_info = sorted(total_odds_info, key=lambda x: x["total"])


        pts = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        home_error = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        # Домашняя команда
        home_team = MLBTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = MLBTeam.objects.filter(team_id=match.team1_id).first()

        ot = (pts.total_i1 + pts.total_i2 + pts.total_i3 + pts.total_i4 + pts.total_i5 + pts.total_i6 + pts.total_i7 + pts.total_i8 + pts.total_i9 + pts.total_i1_missed + pts.total_i2_missed + pts.total_i3_missed + pts.total_i4_missed + pts.total_i5_missed + pts.total_i6_missed + pts.total_i7_missed + pts.total_i8_missed + pts.total_i9_missed) - (pts.total + pts.total_missed)

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_hit": pts.hit if pts else "N/A",
                "away_error": pts.error if pts else "N/A",
                "away_i1": pts.total_i1 if pts else "N/A",
                "away_i2": pts.total_i2 if pts else "N/A",
                "away_i3": pts.total_i3 if pts else "N/A",
                "away_i4": pts.total_i4 if pts else "N/A",
                "away_i5": pts.total_i5 if pts else "N/A",
                "away_i6": pts.total_i6 if pts else "N/A",
                "away_i7": pts.total_i7 if pts else "N/A",
                "away_i8": pts.total_i8 if pts else "N/A",
                "away_i9": pts.total_i9 if pts else "N/A",

                "home_total": pts.total_missed if pts else "N/A",
                "home_hit": pts.hit_missed if pts else "N/A",
                "home_error": home_error.error if home_error else "N/A",
                "home_i1": pts.total_i1_missed if pts else "N/A",
                "home_i2": pts.total_i2_missed if pts else "N/A",
                "home_i3": pts.total_i3_missed if pts else "N/A",
                "home_i4": pts.total_i4_missed if pts else "N/A",
                "home_i5": pts.total_i5_missed if pts else "N/A",
                "home_i6": pts.total_i6_missed if pts else "N/A",
                "home_i7": pts.total_i7_missed if pts else "N/A",
                "home_i8": pts.total_i8_missed if pts else "N/A",
                "home_i9": pts.total_i9_missed if pts else "N/A",
            },

            "periods": periods,
            "total_odds": total_odds_info,

            "ot": ot,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }
    

class MLBMoneylineSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = MLBMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-й Иннинг': 2,
            '2-й Иннинг': 3,
            '3-й Иннинг': 4,
            '4-й Иннинг': 5,
            '5-й Иннинг': 6,
            '2-я Половина': 7,
            '6-й Иннинг': 8,
            '7-й Иннинг': 9,
            '8-й Иннинг': 10,
            '9-й Иннинг': 11,
        }

        moneyline = MLBMoneylineBet.objects.filter(match_id=match.match_id)
        moneyline_info = [{ "period": ml.get_period_display(),
            "home_odds": ml.team2_odds,
            "away_odds": ml.team1_odds,
        } for ml in moneyline]

        moneyline_info = sorted(moneyline_info, key=lambda x: order_map[x['period']])

        pts = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        home_error = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        # Домашняя команда
        home_team = MLBTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = MLBTeam.objects.filter(team_id=match.team1_id).first()

        ot = (pts.total_i1 + pts.total_i2 + pts.total_i3 + pts.total_i4 + pts.total_i5 + pts.total_i6 + pts.total_i7 + pts.total_i8 + pts.total_i9 + pts.total_i1_missed + pts.total_i2_missed + pts.total_i3_missed + pts.total_i4_missed + pts.total_i5_missed + pts.total_i6_missed + pts.total_i7_missed + pts.total_i8_missed + pts.total_i9_missed) - (pts.total + pts.total_missed)

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_hit": pts.hit if pts else "N/A",
                "away_error": pts.error if pts else "N/A",
                "away_i1": pts.total_i1 if pts else "N/A",
                "away_i2": pts.total_i2 if pts else "N/A",
                "away_i3": pts.total_i3 if pts else "N/A",
                "away_i4": pts.total_i4 if pts else "N/A",
                "away_i5": pts.total_i5 if pts else "N/A",
                "away_i6": pts.total_i6 if pts else "N/A",
                "away_i7": pts.total_i7 if pts else "N/A",
                "away_i8": pts.total_i8 if pts else "N/A",
                "away_i9": pts.total_i9 if pts else "N/A",

                "home_total": pts.total_missed if pts else "N/A",
                "home_hit": pts.hit_missed if pts else "N/A",
                "home_error": home_error.error if home_error else "N/A",
                "home_i1": pts.total_i1_missed if pts else "N/A",
                "home_i2": pts.total_i2_missed if pts else "N/A",
                "home_i3": pts.total_i3_missed if pts else "N/A",
                "home_i4": pts.total_i4_missed if pts else "N/A",
                "home_i5": pts.total_i5_missed if pts else "N/A",
                "home_i6": pts.total_i6_missed if pts else "N/A",
                "home_i7": pts.total_i7_missed if pts else "N/A",
                "home_i8": pts.total_i8_missed if pts else "N/A",
                "home_i9": pts.total_i9_missed if pts else "N/A",
            },

            "moneyline_info": moneyline_info,

            "ot": ot,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class MLBHandicapSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = MLBMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        period = self.context.get("period")

        period = MLBHandicapBet._meta.get_field('period').choices

        period_value = MLBHandicapBet._meta.get_field('period').choices[self.context.get("period")][0]


        order_map = {
            'Весь Матч': 0,
            '1-я Половина': 1,
            '1-й Иннинг': 2,
            '2-й Иннинг': 3,
            '3-й Иннинг': 4,
            '4-й Иннинг': 5,
            '5-й Иннинг': 6,
            '2-я Половина': 7,
            '6-й Иннинг': 8,
            '7-й Иннинг': 9,
            '8-й Иннинг': 10,
            '9-й Иннинг': 11,
        }

        period = MLBHandicapBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(MLBHandicapBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(MLBHandicapBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        handicap_odds = MLBHandicapBet.objects.filter(match_id=match.match_id, period=period_value)

        handicap_odds_info = [{ "handicap": h.handicap,
            "handicap_team1_odds": h.handicap_team1_odds,
            "handicap_team2_odds": h.handicap_team2_odds,
            "handicap_team1_result": h.handicap_team1_result,
            "handicap_team2_result": h.handicap_team2_result,
            "period": self.context.get("period"),
        } for h in handicap_odds]

        handicap_odds_info = sorted(handicap_odds_info, key=lambda x: x["handicap"])


        pts = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        home_error = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        # Домашняя команда
        home_team = MLBTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = MLBTeam.objects.filter(team_id=match.team1_id).first()

        ot = (pts.total_i1 + pts.total_i2 + pts.total_i3 + pts.total_i4 + pts.total_i5 + pts.total_i6 + pts.total_i7 + pts.total_i8 + pts.total_i9 + pts.total_i1_missed + pts.total_i2_missed + pts.total_i3_missed + pts.total_i4_missed + pts.total_i5_missed + pts.total_i6_missed + pts.total_i7_missed + pts.total_i8_missed + pts.total_i9_missed) - (pts.total + pts.total_missed)

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_hit": pts.hit if pts else "N/A",
                "away_error": pts.error if pts else "N/A",
                "away_i1": pts.total_i1 if pts else "N/A",
                "away_i2": pts.total_i2 if pts else "N/A",
                "away_i3": pts.total_i3 if pts else "N/A",
                "away_i4": pts.total_i4 if pts else "N/A",
                "away_i5": pts.total_i5 if pts else "N/A",
                "away_i6": pts.total_i6 if pts else "N/A",
                "away_i7": pts.total_i7 if pts else "N/A",
                "away_i8": pts.total_i8 if pts else "N/A",
                "away_i9": pts.total_i9 if pts else "N/A",

                "home_total": pts.total_missed if pts else "N/A",
                "home_hit": pts.hit_missed if pts else "N/A",
                "home_error": home_error.error if home_error else "N/A",
                "home_i1": pts.total_i1_missed if pts else "N/A",
                "home_i2": pts.total_i2_missed if pts else "N/A",
                "home_i3": pts.total_i3_missed if pts else "N/A",
                "home_i4": pts.total_i4_missed if pts else "N/A",
                "home_i5": pts.total_i5_missed if pts else "N/A",
                "home_i6": pts.total_i6_missed if pts else "N/A",
                "home_i7": pts.total_i7_missed if pts else "N/A",
                "home_i8": pts.total_i8_missed if pts else "N/A",
                "home_i9": pts.total_i9_missed if pts else "N/A",
            },

            "periods": periods,
            "handicap_odds": handicap_odds_info,

            "ot": ot,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class MLBMatchesSchedule(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = MLBMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор


        pts = MLBTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        # Домашняя команда
        home_team = MLBTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = MLBTeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
            },
        }


class MLBTeamStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = MLBTeam
        fields = ['team_id', 'name', 'logo']


class MLBPlayerStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLBPlayer
        fields = ['player_id', 'name']


class MLBStandingsSerializer(serializers.ModelSerializer):
    wins = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()
    home_record = serializers.SerializerMethodField()
    away_record = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    avg_conceded = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = MLBTeam
        fields = [
            "team_id", "logo", "name", "league",
            "wins", "losses", "home_record", "away_record",
            "avg_score", "avg_conceded",
        ]

    def _get_match_ids(self, team):
        season = self.context.get("season")
        return MLBMatch.objects.filter(
            season=season,
            stage__in=["regular", "world tour"]
        ).exclude(stage="all-star").filter(
            Q(team1=team) | Q(team2=team)
        ).values_list("match_id", flat=True)
    
    def get_logo(self, team):
        request = self.context.get("request")
        if team.logo:
            return request.build_absolute_uri(team.logo.url)
        return None

    def _get_results(self, team):
        match_ids = self._get_match_ids(team)

        stats = MLBTeamStat.objects.filter(
            match_id__in=match_ids,
            team=team,
        )

        wins = losses = home_wins = home_losses = away_wins = away_losses = 0
        for s in stats:
            is_home = s.status == "home"
            if s.result == "win":
                wins += 1
                home_wins += int(is_home)
                away_wins += int(not is_home)
            elif s.result == "lose":
                losses += 1
                home_losses += int(is_home)
                away_losses += int(not is_home)

        return {
            "wins": wins, "losses": losses,
            "home_wins": home_wins, "home_losses": home_losses,
            "away_wins": away_wins, "away_losses": away_losses
        }

    def get_wins(self, team):
        return self._get_results(team)["wins"]

    def get_losses(self, team):
        return self._get_results(team)["losses"]

    def get_home_record(self, team):
        r = self._get_results(team)
        return f"{r['home_wins']}-{r['home_losses']}"

    def get_away_record(self, team):
        r = self._get_results(team)
        return f"{r['away_wins']}-{r['away_losses']}"
    
    def get_avg_score(self, team):
        match_ids = self._get_match_ids(team)
        pts = MLBTeamPtsStat.objects.filter(match_id__in=match_ids, team=team)
        total = sum(p.total or 0 for p in pts)
        count = pts.count()
        return round(total / count, 2) if count > 0 else 0.0
    
    def get_avg_conceded(self, team):
        match_ids = self._get_match_ids(team)
        pts = MLBTeamPtsStat.objects.filter(match_id__in=match_ids, team=team)
        total = sum(p.total_missed or 0 for p in pts)
        count = pts.count()
        return round(total / count, 2) if count > 0 else 0.0
