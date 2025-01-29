from django.db import models
import uuid

class NFLTeam(models.Model):
    team_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nfl_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NFLMatch(models.Model):
    match_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(NFLTeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NFLTeam, related_name='away_matches', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    stage = models.CharField(max_length=20)
    week = models.IntegerField()

    class Meta():
        db_table = 'nfl_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NFLTeamStat(models.Model):
    team_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    class Meta():
        db_table = 'nfl_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NFLTeamPtsStat(models.Model):
    team_pts_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    total = models.IntegerField()
    totalMissed = models.IntegerField()
    total_Q1 = models.IntegerField()
    total_Q1Missed = models.IntegerField()
    total_Q2 = models.IntegerField()
    total_Q2Missed = models.IntegerField()
    total_Q3 = models.IntegerField()
    total_Q3Missed = models.IntegerField()
    total_Q4 = models.IntegerField()
    total_Q4Missed = models.IntegerField()

    class Meta():
        db_table = 'nfl_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NFLPlayer(models.Model):
    player_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nfl_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NFLPlayerStat(models.Model):
    stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NFLPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    C = models.IntegerField()
    ATT = models.IntegerField()
    YDS = models.IntegerField()
    AVG = models.FloatField()
    TD = models.IntegerField()
    interception = models.IntegerField()
    SACK = models.IntegerField()
    trying_SACK = models.IntegerField()
    QBR = models.FloatField()
    RTG = models.FloatField()
    CAR = models.IntegerField()
    LONG = models.IntegerField()
    REC = models.IntegerField()
    TGTS = models.IntegerField()
    FUM = models.IntegerField()
    LOST = models.IntegerField()
    TOT = models.IntegerField()
    SOLO = models.IntegerField()
    SACKS = models.IntegerField()
    TFL = models.IntegerField()
    PD = models.IntegerField()
    QB_HTS = models.IntegerField()
    NO = models.IntegerField()
    FG = models.IntegerField()
    trying_FG = models.IntegerField()
    PCT = models.IntegerField()
    XP = models.IntegerField()
    trying_XP = models.IntegerField()
    PTS = models.IntegerField()
    TB = models.IntegerField()
    In_20 = models.IntegerField()

    class Meta():
        db_table = 'nfl_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NFLBet(models.Model):
    bet_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team1 = models.ForeignKey(NFLTeam, related_name='bets_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NFLTeam, related_name='bets_as_team2', on_delete=models.CASCADE)
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
        db_table = 'nfl_bet'
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['week']),
    ]
