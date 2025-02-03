from django.db import models
import uuid

class NFLTeam(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nfl_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NFLMatch(models.Model):
    match_id = models.CharField(max_length=20, primary_key=True, editable=False)
    team1 = models.ForeignKey(NFLTeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NFLTeam, related_name='away_matches', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    stage = models.CharField(max_length=50)
    week = models.IntegerField()
    season_type = models.IntegerField(null=True, blank=True)

    class Meta():
        db_table = 'nfl_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NFLTeamStat(models.Model):
    team_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    class Meta():
        db_table = 'nfl_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NFLTeamPtsStat(models.Model):
    team_pts_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    total = models.IntegerField()
    total_missed = models.IntegerField()
    total_q1 = models.IntegerField()
    total_q1_missed = models.IntegerField()
    total_q2 = models.IntegerField()
    total_q2_missed = models.IntegerField()
    total_q3 = models.IntegerField()
    total_q3_missed = models.IntegerField()
    total_q4 = models.IntegerField()
    total_q4_missed = models.IntegerField()

    class Meta():
        db_table = 'nfl_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NFLPlayer(models.Model):
    player_id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nfl_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NFLPlayerStat(models.Model):
    stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NFLPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    c = models.IntegerField(null = True)
    att = models.IntegerField(null = True)
    yds = models.IntegerField(null = True)
    avg = models.FloatField(null = True)
    td = models.IntegerField(null = True)
    interception = models.IntegerField(null = True)
    sack = models.IntegerField(null = True)
    trying_sack = models.IntegerField(null = True)
    qbr = models.FloatField(null = True)
    rtg = models.FloatField(null = True)
    car = models.IntegerField(null = True)
    long = models.IntegerField(null = True)
    rec = models.IntegerField(null = True)
    tgts = models.IntegerField(null = True)
    fum = models.IntegerField(null = True)
    lost = models.IntegerField(null = True)
    tot = models.IntegerField(null = True)
    solo = models.IntegerField(null = True)
    sacks = models.IntegerField(null = True)
    tfl = models.IntegerField(null = True)
    pd = models.IntegerField(null = True)
    qb_hts = models.IntegerField(null = True)
    no = models.IntegerField(null = True)
    fg = models.IntegerField(null = True)
    trying_fg = models.IntegerField(null = True)
    pct = models.IntegerField(null = True)
    xp = models.IntegerField(null = True)
    trying_xp = models.IntegerField(null = True)
    pts = models.IntegerField(null = True)
    tb = models.IntegerField(null = True)
    in_20 = models.IntegerField(null = True)

    class Meta():
        db_table = 'nfl_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NFLBet(models.Model):
    bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NFLMatch, on_delete=models.CASCADE)
    team1 = models.ForeignKey(NFLTeam, related_name='bets_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NFLTeam, related_name='bets_as_team2', on_delete=models.CASCADE)
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
        db_table = 'nfl_bet'
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

class NFLUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)  # Автоматически обновляется при изменении записи

    class Meta:
        db_table = 'nfl_update'
        verbose_name = "Обновление NFL"
        verbose_name_plural = "Обновления NFL"

    def __str__(self):
        return f"Обновлено: {self.updated_at.strftime('%d-%m-%Y %H:%M:%S')}"

class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['week']),
    ]
