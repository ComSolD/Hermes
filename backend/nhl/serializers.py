from rest_framework import serializers
from nhl.models import NHLHandicapBet, NHLPlayer, NHLPlayerStat, NHLTeamPtsStat, NHLTeamStat, NHLMatch, NHLMoneylineBet, NHLXBet, NHLTeam, NHLTotalBet
from django.db.models import Q

class NHLMatchSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1    

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

            # Нападающие
        home_forward_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="forward")

        home_forward_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "g": p.g,
            "a": p.a,
            "plus_minus": p.plus_minus,
            "s": p.s,
            "sm": p.sm,
            "bs": p.bs,
            "pn": p.pn,
            "pim": p.pim,
            "ht": p.ht,
            "tk": p.tk,
            "gv": p.gv,
        } for p in home_forward_players]

            # Защитники
        home_defenseman_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="defenseman")

        home_defenseman_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "g": p.g,
            "a": p.a,
            "plus_minus": p.plus_minus,
            "s": p.s,
            "sm": p.sm,
            "bs": p.bs,
            "pn": p.pn,
            "pim": p.pim,
            "ht": p.ht,
            "tk": p.tk,
            "gv": p.gv,
        } for p in home_defenseman_players]

            # Вратари
        home_goalie_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team2_id, position="goalie")

        home_goalie_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "sa": p.sa,
            "ga": p.ga,
            "sv": p.sv,
            "sv_procent": p.sv_procent,
            "essv": p.essv,
            "ppsv": p.ppsv,
        } for p in home_goalie_players]

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

            # Нападающие
        away_forward_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="forward")

        away_forward_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "g": p.g,
            "a": p.a,
            "plus_minus": p.plus_minus,
            "s": p.s,
            "sm": p.sm,
            "bs": p.bs,
            "pn": p.pn,
            "pim": p.pim,
            "ht": p.ht,
            "tk": p.tk,
            "gv": p.gv,
        } for p in away_forward_players]


            # Защитники
        away_defenseman_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="defenseman")

        away_defenseman_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "g": p.g,
            "a": p.a,
            "plus_minus": p.plus_minus,
            "s": p.s,
            "sm": p.sm,
            "bs": p.bs,
            "pn": p.pn,
            "pim": p.pim,
            "ht": p.ht,
            "tk": p.tk,
            "gv": p.gv,
        } for p in away_defenseman_players]

            # Вратари
        away_goalie_players = NHLPlayerStat.objects.filter(match_id=match.match_id, team_id=match.team1_id, position="goalie")

        away_goalie_players_info = [{"player": NHLPlayer.objects.filter(player_id=p.player.player_id).first().name, 
            "sa": p.sa,
            "ga": p.ga,
            "sv": p.sv,
            "sv_procent": p.sv_procent,
            "essv": p.essv,
            "ppsv": p.ppsv,
        } for p in away_goalie_players]


        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "match_status": match_status.status if match_status else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_p1": pts.total_p1 if pts else "N/A",
                "away_p2": pts.total_p2 if pts else "N/A",
                "away_p3": pts.total_p3 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_p1": pts.total_p1_missed if pts else "N/A",
                "home_p2": pts.total_p2_missed if pts else "N/A",
                "home_p3": pts.total_p3_missed if pts else "N/A",
            },

            "home_forward_players": home_forward_players_info,
            "home_defenseman_players": home_defenseman_players_info,
            "home_goalie_players": home_goalie_players_info,
            

            "away_forward_players": away_forward_players_info,
            "away_defenseman_players": away_defenseman_players_info,
            "away_goalie_players": away_goalie_players_info,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NHLTotalSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        period = self.context.get("period")

        period = NHLTotalBet._meta.get_field('period').choices

        period_value = NHLTotalBet._meta.get_field('period').choices[self.context.get("period")][0]

        order_map = {
            'Весь Матч': 0,
            '1-й Период': 1,
            '2-й Период': 2,
            '3-й Период': 3,
        }

        period = NHLTotalBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(NHLTotalBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(NHLTotalBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        total_odds = NHLTotalBet.objects.filter(match_id=match.match_id, period=period_value)

        total_odds_info = [{ "total": to.total,
            "over_odds": to.over_odds,
            "under_odds": to.under_odds,
            "total_result": to.total_result,
            "period": self.context.get("period"),
        } for to in total_odds]

        total_odds_info = sorted(total_odds_info, key=lambda x: x["total"])


        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "match_status": match_status.status if match_status else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_p1": pts.total_p1 if pts else "N/A",
                "away_p2": pts.total_p2 if pts else "N/A",
                "away_p3": pts.total_p3 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_p1": pts.total_p1_missed if pts else "N/A",
                "home_p2": pts.total_p2_missed if pts else "N/A",
                "home_p3": pts.total_p3_missed if pts else "N/A",
            },

            "periods": periods,
            "total_odds": total_odds_info,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NHL1x2Serializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        order_map = {
            'Весь Матч': 0,
            '1-й Период': 1,
            '2-й Период': 2,
            '3-й Период': 3,
        }

        xbet = NHLXBet.objects.filter(match_id=match.match_id)
        xbet_info = [{ "period": ml.get_period_display(),
            "home_odds": ml.team2_odds,
            "draw": ml.draw,
            "away_odds": ml.team1_odds,
        } for ml in xbet]

        xbet_info = sorted(xbet_info, key=lambda x: order_map[x['period']])

        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "match_status": match_status.status if match_status else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_p1": pts.total_p1 if pts else "N/A",
                "away_p2": pts.total_p2 if pts else "N/A",
                "away_p3": pts.total_p3 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_p1": pts.total_p1_missed if pts else "N/A",
                "home_p2": pts.total_p2_missed if pts else "N/A",
                "home_p3": pts.total_p3_missed if pts else "N/A",
            },

            "xbet_info": xbet_info,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NHLMoneylineSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        order_map = {
            'Весь Матч': 0,
            '1-й Период': 1,
            '2-й Период': 2,
            '3-й Период': 3,
        }

        moneyline = NHLMoneylineBet.objects.filter(match_id=match.match_id)
        moneyline_info = [{ "period": ml.get_period_display(),
            "home_odds": ml.team2_odds,
            "away_odds": ml.team1_odds,
        } for ml in moneyline]

        moneyline_info = sorted(moneyline_info, key=lambda x: order_map[x['period']])

        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "match_status": match_status.status if match_status else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_p1": pts.total_p1 if pts else "N/A",
                "away_p2": pts.total_p2 if pts else "N/A",
                "away_p3": pts.total_p3 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_p1": pts.total_p1_missed if pts else "N/A",
                "home_p2": pts.total_p2_missed if pts else "N/A",
                "home_p3": pts.total_p3_missed if pts else "N/A",
            },

            "moneyline_info": moneyline_info,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NHLHandicapSerializer(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        match = obj  # Здесь уже передан нужный матч через сериализатор

        request = self.context.get("request")

        period = self.context.get("period")

        period = NHLHandicapBet._meta.get_field('period').choices

        period_value = NHLHandicapBet._meta.get_field('period').choices[self.context.get("period")][0]


        order_map = {
            'Весь Матч': 0,
            '1-й Период': 1,
            '2-й Период': 2,
            '3-й Период': 3,
        }

        period = NHLHandicapBet.objects.filter(match_id=match.match_id).values_list('period', flat=True).distinct()

        periods = [{"period": dict(NHLHandicapBet._meta.get_field('period').choices)[p],
            "number": order_map[dict(NHLHandicapBet._meta.get_field('period').choices)[p]]
        } for p in period]

        periods = sorted(periods, key=lambda x: order_map[x['period']])


        handicap_odds = NHLHandicapBet.objects.filter(match_id=match.match_id, period=period_value)

        handicap_odds_info = [{ "handicap": h.handicap,
            "handicap_team1_odds": h.handicap_team1_odds,
            "handicap_team2_odds": h.handicap_team2_odds,
            "handicap_team1_result": h.handicap_team1_result,
            "handicap_team2_result": h.handicap_team2_result,
            "period": self.context.get("period"),
        } for h in handicap_odds]

        handicap_odds_info = sorted(handicap_odds_info, key=lambda x: x["handicap"])


        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()

        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "match_status": match_status.status if match_status else "Unknown",
            "home_team_logo": request.build_absolute_uri(home_team.logo.url) if home_team.logo else None,
            "away_team_logo": request.build_absolute_uri(away_team.logo.url) if away_team.logo else None,
            "total": {
                "away_total": pts.total if pts else "N/A",
                "away_p1": pts.total_p1 if pts else "N/A",
                "away_p2": pts.total_p2 if pts else "N/A",
                "away_p3": pts.total_p3 if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
                "home_p1": pts.total_p1_missed if pts else "N/A",
                "home_p2": pts.total_p2_missed if pts else "N/A",
                "home_p3": pts.total_p3_missed if pts else "N/A",
            },

            "periods": periods,
            "handicap_odds": handicap_odds_info,

            "stage": match.get_stage_display(),

            "time": match.time.strftime("%H:%M"),

            "date": match.date.strftime("%d-%m-%Y"),
        }


class NHLMatchesSchedule(serializers.ModelSerializer):
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = NHLMatch
        fields = '__all__'

    def get_match_info(self, obj):
        """Форматирует информацию о конкретном матче."""
        
        match = obj  # Здесь уже передан нужный матч через сериализатор


        pts = NHLTeamPtsStat.objects.filter(match_id=match.match_id, team_id=match.team1_id).first()

        match_status = NHLMatch.objects.filter(match_id=match.match_id).first()

        # Домашняя команда
        home_team = NHLTeam.objects.filter(team_id=match.team2_id).first()

        # Выездная команда
        away_team = NHLTeam.objects.filter(team_id=match.team1_id).first()

        home_result = NHLTeamStat.objects.filter(match_id=match.match_id, team_id=match.team2_id).first()


        if match_status.status != "Maintime" and home_result.result == "win":
            pts.total_missed += 1
        elif match_status.status != "Maintime" and home_result.result == "lose":
            pts.total += 1        

        return {
            "match_id": match.match_id,
            "home_team": home_team.name if home_team else "Unknown",
            "away_team": away_team.name if away_team else "Unknown",
            "match_status": match_status.status if match_status else "Unknown",
            "total": {
                "away_total": pts.total if pts else "N/A",
                "home_total": pts.total_missed if pts else "N/A",
            },
        }


class NHLTeamStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = NHLTeam
        fields = ['team_id', 'name', 'logo']


class NHLPlayerStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHLPlayer
        fields = ['player_id', 'name']


class NHLStandingsSerializer(serializers.ModelSerializer):
    wins = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()
    home_record = serializers.SerializerMethodField()
    away_record = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    avg_conceded = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = NHLTeam
        fields = [
            "team_id", "logo", "name", "league",
            "wins", "losses", "home_record", "away_record",
            "avg_score", "avg_conceded",
        ]

    def _get_match_ids(self, team):
        season = self.context.get("season")
        return NHLMatch.objects.filter(
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

        stats = NHLTeamStat.objects.filter(
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
        pts = NHLTeamPtsStat.objects.filter(match_id__in=match_ids, team=team)
        total = sum(p.total or 0 for p in pts)
        count = pts.count()
        return round(total / count, 2) if count > 0 else 0.0
    
    def get_avg_conceded(self, team):
        match_ids = self._get_match_ids(team)
        pts = NHLTeamPtsStat.objects.filter(match_id__in=match_ids, team=team)
        total = sum(p.total_missed or 0 for p in pts)
        count = pts.count()
        return round(total / count, 2) if count > 0 else 0.0

