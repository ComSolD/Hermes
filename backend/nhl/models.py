from django.db import models
import uuid

class NHLTeam(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nhl_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NHLMatch(models.Model):
    match_id = models.CharField(max_length=20,primary_key=True, editable=False)
    team1 = models.ForeignKey(NHLTeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NHLTeam, related_name='away_matches', on_delete=models.CASCADE)
    status = models.CharField(null=True, blank=True, max_length=20)
    season = models.CharField(max_length=10)
    stage = models.CharField(max_length=20)
    date = models.DateField()

    class Meta():
        db_table = 'nhl_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NHLTeamStat(models.Model):
    team_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    class Meta():
        db_table = 'nhl_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NHLTeamPtsStat(models.Model):
    team_pts_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    total = models.IntegerField()
    total_missed = models.IntegerField()
    total_t1 = models.IntegerField()
    total_t1_missed = models.IntegerField()
    total_t2 = models.IntegerField()
    total_t2_missed = models.IntegerField()
    total_t3 = models.IntegerField()
    total_t3_missed = models.IntegerField()

    class Meta():
        db_table = 'nhl_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NHLPlayer(models.Model):
    player_id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nhl_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NHLPlayerStat(models.Model):
    stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NHLPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=20)
    g = models.IntegerField(null = True)
    a = models.IntegerField(null = True)
    plus_minus = models.IntegerField(null = True)
    s = models.IntegerField(null = True)
    sm = models.IntegerField(null = True)
    bs = models.IntegerField(null = True)
    pn = models.IntegerField(null = True)
    pim = models.IntegerField(null = True)
    ht = models.IntegerField(null = True)
    tk = models.IntegerField(null = True)
    gv = models.IntegerField(null = True)
    sa = models.IntegerField(null = True)
    ga = models.IntegerField(null = True)
    sv = models.IntegerField(null = True)
    sv_procent = models.IntegerField(null = True)
    essv = models.IntegerField(null = True)
    ppsv = models.IntegerField(null = True)

    class Meta():
        db_table = 'nhl_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NHLBet(models.Model):
    bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team1 = models.ForeignKey(NHLTeam, related_name='bets_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NHLTeam, related_name='bets_as_team2', on_delete=models.CASCADE)
    ml_team1_parlay = models.FloatField(null=True, blank=True)
    ml_team2_parlay = models.FloatField(null=True, blank=True)
    ml_result = models.CharField(max_length=36, null=True, blank=True)
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

class NHLUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)  # Автоматически обновляется при изменении записи

    class Meta:
        db_table = 'nhl_update'
        verbose_name = "Обновление NHL"
        verbose_name_plural = "Обновления NHL"

    def __str__(self):
        return f"Обновлено: {self.updated_at.strftime('%d-%m-%Y %H:%M:%S')}"

class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['date']),
    ]
