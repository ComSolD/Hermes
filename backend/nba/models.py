from django.db import models
import uuid

class NBATeam(models.Model):
    team_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nba_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NBAMatch(models.Model):
    match_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(NBATeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NBATeam, related_name='away_matches', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    stage = models.CharField(max_length=20)
    date = models.DateField()

    class Meta():
        db_table = 'nba_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NBATeamStat(models.Model):
    team_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    FG = models.IntegerField()
    trying_FG = models.IntegerField()
    three_PT = models.IntegerField()
    attempted_three_PT = models.IntegerField()
    FT = models.IntegerField()
    trying_FT = models.IntegerField()
    OREB = models.IntegerField()
    DREB = models.IntegerField()
    REB = models.IntegerField()
    AST = models.IntegerField()
    STL = models.IntegerField()
    BLK = models.IntegerField()
    turnovers = models.IntegerField()
    PF = models.IntegerField()

    class Meta():
        db_table = 'nba_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NBATeamPtsStat(models.Model):
    team_pts_stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
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
        db_table = 'nba_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NBAPlayer(models.Model):
    player_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nba_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NBAPlayerStat(models.Model):
    stat_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NBAPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    PTS = models.IntegerField()
    FG = models.IntegerField()
    trying_FG = models.IntegerField()
    three_PT = models.IntegerField()
    attempted_three_PT = models.IntegerField()
    FT = models.IntegerField()
    trying_FT = models.IntegerField()
    OREB = models.IntegerField()
    DREB = models.IntegerField()
    REB = models.IntegerField()
    AST = models.IntegerField()
    STL = models.IntegerField()
    BLK = models.IntegerField()
    turnovers = models.IntegerField()
    PF = models.IntegerField()
    plusMinus = models.IntegerField()
    MIN = models.IntegerField()

    class Meta():
        db_table = 'nba_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NBABet(models.Model):
    bet_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team1 = models.ForeignKey(NBATeam, related_name='bets_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NBATeam, related_name='bets_as_team2', on_delete=models.CASCADE)
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
        db_table = 'nba_bet'
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

# Добавление индексов для ускорения поиска
class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['date']),
    ]
