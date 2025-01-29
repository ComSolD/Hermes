from django.db import models
import uuid

class NHLTeam(models.Model):
    team_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nhl_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NHLMatch(models.Model):
    match_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(NHLTeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NHLTeam, related_name='away_matches', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    season = models.CharField(max_length=10)
    stage = models.CharField(max_length=20)
    date = models.DateField()

    class Meta():
        db_table = 'nhl_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NHLTeamStat(models.Model):
    team_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    class Meta():
        db_table = 'nhl_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NHLTeamPtsStat(models.Model):
    team_pts_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    total = models.IntegerField()
    totalMissed = models.IntegerField()
    total_T1 = models.IntegerField()
    total_T1Missed = models.IntegerField()
    total_T2 = models.IntegerField()
    total_T2Missed = models.IntegerField()
    total_T3 = models.IntegerField()
    total_T3Missed = models.IntegerField()

    class Meta():
        db_table = 'nhl_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NHLPlayer(models.Model):
    player_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nhl_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NHLPlayerStat(models.Model):
    stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NHLPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    G = models.IntegerField()
    A = models.IntegerField()
    plusMinus = models.IntegerField()
    S = models.IntegerField()
    SM = models.IntegerField()
    BS = models.IntegerField()
    PN = models.IntegerField()
    PIM = models.IntegerField()
    HT = models.IntegerField()
    TK = models.IntegerField()
    GV = models.IntegerField()
    SA = models.IntegerField()
    GA = models.IntegerField()
    SV = models.IntegerField()
    SVProcent = models.IntegerField()
    ESSV = models.IntegerField()
    PPSV = models.IntegerField()

    class Meta():
        db_table = 'nhl_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NHLBet(models.Model):
    bet_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team1 = models.ForeignKey(NHLTeam, related_name='bets_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NHLTeam, related_name='bets_as_team2', on_delete=models.CASCADE)
    ML_team1_parlay = models.FloatField(null=True, blank=True)
    ML_team2_parlay = models.FloatField(null=True, blank=True)
    ML_result = models.CharField(max_length=36, null=True, blank=True)
    total = models.FloatField()
    over_total_parlay = models.FloatField(null=True, blank=True)
    under_total_parlay = models.FloatField(null=True, blank=True)
    total_result = models.CharField(max_length=10, null=True, blank=True)
    spread_team1 = models.FloatField(null=True, blank=True)
    spread_team1_parlay = models.FloatField(null=True, blank=True)
    spread_team2 = models.FloatField(null=True, blank=True)
    spread_team2_parlay = models.FloatField(null=True, blank=True)
    spread_result = models.CharField(max_length=36, null=True, blank=True)

    class Meta():
        db_table = 'nhl_bet'
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['date']),
    ]
