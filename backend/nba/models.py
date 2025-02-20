from enum import unique
from django.db import models
import uuid

class NBATeam(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nba_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class NBAMatch(models.Model):
    match_id = models.CharField(max_length=200, primary_key=True, editable=False)
    team1 = models.ForeignKey(NBATeam, related_name='away_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NBATeam, related_name='home_matches', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    stage = models.CharField(null=True, blank=True, max_length=50)
    date = models.DateField()

    class Meta():
        db_table = 'nba_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class NBATeamStat(models.Model):

    RESULT_CHOICES = [
        ('win', 'Победа'),
        ('lose', 'Проигрышь'),
        ('draw', 'Ничья')
    ]

    STATUS_CHOICES = [
        ('home', 'Дом'),
        ('away', 'Выезд')
    ]

    team_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    fg = models.IntegerField(null = True)
    trying_fg = models.IntegerField(null = True)
    three_pt = models.IntegerField(null = True)
    attempted_three_pt = models.IntegerField(null = True)
    ft = models.IntegerField(null = True)
    trying_ft = models.IntegerField(null = True)
    oreb = models.IntegerField(null = True)
    dreb = models.IntegerField(null = True)
    reb = models.IntegerField(null = True)
    ast = models.IntegerField(null = True)
    stl = models.IntegerField(null = True)
    blk = models.IntegerField(null = True)
    turnovers = models.IntegerField(null = True)
    pf = models.IntegerField(null = True)

    class Meta():
        db_table = 'nba_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class NBATeamPtsStat(models.Model):
    team_pts_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
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
        db_table = 'nba_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class NBAPlayer(models.Model):
    player_id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'nba_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class NBAPlayerStat(models.Model):

    POSITION_CHOICES = [
        ('starter', 'Стартер'),
        ('bench', 'Скамейка')
    ]

    stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NBAPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    pts = models.IntegerField(null = True)
    fg = models.IntegerField(null = True)
    trying_fg = models.IntegerField(null = True)
    three_pt = models.IntegerField(null = True)
    attempted_three_pt = models.IntegerField(null = True)
    ft = models.IntegerField(null = True)
    trying_ft = models.IntegerField(null = True)
    oreb = models.IntegerField(null = True)
    dreb = models.IntegerField(null = True)
    reb = models.IntegerField(null = True)
    ast = models.IntegerField(null = True)
    stl = models.IntegerField(null = True)
    blk = models.IntegerField(null = True)
    turnovers = models.IntegerField(null = True)
    pf = models.IntegerField(null = True)
    plus_minus = models.IntegerField(null = True)
    min = models.IntegerField(null = True)

    class Meta():
        db_table = 'nba_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NBAMoneylineBet(models.Model):
    moneyline_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('2nd_half', '2-я Половина'),
            ('1st_quarter', '1-я Четверть'),
            ('2nd_quarter', '2-я Четверть'),
            ('3rd_quarter', '3-я Четверть'),
            ('4th_quarter', '4-я Четверть'),
        ]
    )

    team1_odds = models.FloatField(null=True, blank=True)
    team2_odds = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=36, null=True, blank=True)


    class Meta():
        db_table = 'nba_moneyline_bet'
        verbose_name = 'Ставка на победу'
        verbose_name_plural = 'Ставки на победу'

class NBATotalBet(models.Model):
    total_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('2nd_half', '2-я Половина'),
            ('1st_quarter', '1-я Четверть'),
            ('2nd_quarter', '2-я Четверть'),
            ('3rd_quarter', '3-я Четверть'),
            ('4th_quarter', '4-я Четверть'),
        ]
    )

    total = models.FloatField()
    over_odds = models.FloatField(null=True, blank=True)
    under_odds = models.FloatField(null=True, blank=True)
    total_result = models.CharField(max_length=10, null=True, blank=True)

    class Meta():
        db_table = 'nba_total_bet'
        verbose_name = 'Ставка на тотал'
        verbose_name_plural = 'Ставки на тоталы'

class NBAHandicapBet(models.Model):
    handicap_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NBAMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('2nd_half', '2-я Половина'),
            ('1st_quarter', '1-я Четверть'),
            ('2nd_quarter', '2-я Четверть'),
            ('3rd_quarter', '3-я Четверть'),
            ('4th_quarter', '4-я Четверть'),
        ]
    )
    handicap = models.FloatField(null=True, blank=True)
    handicap_team1_odds = models.FloatField(null=True, blank=True)
    handicap_team2_odds = models.FloatField(null=True, blank=True)
    handicap_result = models.CharField(max_length=36, null=True, blank=True)

    class Meta():
        db_table = 'nba_handicap_bet'
        verbose_name = 'Ставка на фору'
        verbose_name_plural = 'Ставки на форы'

class NBAUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)  # Автоматически обновляется при изменении записи

    class Meta:
        db_table = 'nba_update'
        verbose_name = "Обновление NBA"
        verbose_name_plural = "Обновления NBA"

    def __str__(self):
        return f"Обновлено: {self.updated_at.strftime('%d-%m-%Y %H:%M:%S')}"


# Добавление индексов для ускорения поиска
class Meta:
    indexes = [
        models.Index(fields=['match']),
        models.Index(fields=['team']),
        models.Index(fields=['player']),
        models.Index(fields=['date']),
    ]
