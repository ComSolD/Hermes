from django.db import models
import uuid

class MLBTeam(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'mlb_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class MLBMatch(models.Model):
    match_id = models.CharField(max_length=200, primary_key=True, editable=False)
    team1 = models.ForeignKey(MLBTeam, related_name='away_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(MLBTeam, related_name='home_matches', on_delete=models.CASCADE)
    season = models.CharField(max_length=10)
    stage = models.CharField(null=True, blank=True, max_length=50)
    date = models.DateField()

    class Meta():
        db_table = 'mlb_match'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

class MLBTeamStat(models.Model):

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
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(MLBTeam, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta():
        db_table = 'mlb_team_stat'
        verbose_name = 'Статистика команды'
        verbose_name_plural = 'Статистика команд'

class MLBTeamPtsStat(models.Model):
    team_pts_stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(MLBTeam, on_delete=models.CASCADE)
    run = models.IntegerField()
    run_missed = models.IntegerField()
    hit = models.IntegerField()
    hit_missed = models.IntegerField()
    error = models.IntegerField()
    run_i1 = models.IntegerField()
    run_i1_missed = models.IntegerField()
    run_i2 = models.IntegerField()
    run_i2_missed = models.IntegerField()
    run_i3 = models.IntegerField()
    run_i3_missed = models.IntegerField()
    run_i4 = models.IntegerField()
    run_i4_missed = models.IntegerField()
    run_i5 = models.IntegerField()
    run_i5_missed = models.IntegerField()
    run_i6 = models.IntegerField()
    run_i6_missed = models.IntegerField()
    run_i7 = models.IntegerField()
    run_i7_missed = models.IntegerField()
    run_i8 = models.IntegerField()
    run_i8_missed = models.IntegerField()
    run_i9 = models.IntegerField()
    run_i9_missed = models.IntegerField()

    class Meta():
        db_table = 'mlb_team_pts_stat'
        verbose_name = 'Статистика команды по очкам'
        verbose_name_plural = 'Статистика команд по очкам'

class MLBPlayer(models.Model):
    player_id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'mlb_player'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

class MLBPlayerStat(models.Model):

    POSITION_CHOICES = [
        ('hitter', 'Бьющий'),
        ('pitcher ', 'Подающий')
    ]

    stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(MLBPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(MLBTeam, on_delete=models.CASCADE)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    role = models.CharField(max_length=10)

    ab = models.IntegerField(null = True)
    r = models.IntegerField(null = True)
    h = models.IntegerField(null = True)
    rbi = models.IntegerField(null = True)
    hr = models.IntegerField(null = True)
    bb = models.IntegerField(null = True)
    k = models.IntegerField(null = True)
    avg = models.IntegerField(null = True)
    obp = models.IntegerField(null = True)
    slg = models.IntegerField(null = True)
    ip = models.IntegerField(null = True)
    er = models.IntegerField(null = True)
    pc = models.IntegerField(null = True)
    st = models.IntegerField(null = True)
    era = models.IntegerField(null = True)

    class Meta():
        db_table = 'mlb_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class MLBMoneylineBet(models.Model):
    moneyline_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('1st_inning', '1-й Иннинг'),
            ('2nd_inning', '2-й Иннинг'),
            ('3rd_inning', '3-й Иннинг'),
            ('4th_inning', '4-й Иннинг'),
            ('5th_inning', '4-й Иннинг'),
            ('2nd_half', '2-я Половина'),
            ('6th_inning', '4-й Иннинг'),
            ('7th_inning', '4-й Иннинг'),
            ('8th_inning', '4-й Иннинг'),
            ('9th_inning', '4-й Иннинг'),
        ]
    )

    team1_odds = models.FloatField(null=True, blank=True)
    team2_odds = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=36, null=True, blank=True)


    class Meta():
        db_table = 'mlb_moneyline_bet'
        verbose_name = 'Ставка на победу'
        verbose_name_plural = 'Ставки на победу'

class MLBTotalBet(models.Model):
    total_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('1st_inning', '1-й Иннинг'),
            ('2nd_inning', '2-й Иннинг'),
            ('3rd_inning', '3-й Иннинг'),
            ('4th_inning', '4-й Иннинг'),
            ('5th_inning', '4-й Иннинг'),
            ('2nd_half', '2-я Половина'),
            ('6th_inning', '4-й Иннинг'),
            ('7th_inning', '4-й Иннинг'),
            ('8th_inning', '4-й Иннинг'),
            ('9th_inning', '4-й Иннинг'),
        ]
    )

    total = models.FloatField()
    over_odds = models.FloatField(null=True, blank=True)
    under_odds = models.FloatField(null=True, blank=True)
    total_result = models.CharField(max_length=10, null=True, blank=True)

    class Meta():
        db_table = 'mlb_total_bet'
        verbose_name = 'Ставка на тотал'
        verbose_name_plural = 'Ставки на тоталы'

class MLBHandicapBet(models.Model):
    handicap_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_half', '1-я Половина'),
            ('1st_inning', '1-й Иннинг'),
            ('2nd_inning', '2-й Иннинг'),
            ('3rd_inning', '3-й Иннинг'),
            ('4th_inning', '4-й Иннинг'),
            ('5th_inning', '4-й Иннинг'),
            ('2nd_half', '2-я Половина'),
            ('6th_inning', '4-й Иннинг'),
            ('7th_inning', '4-й Иннинг'),
            ('8th_inning', '4-й Иннинг'),
            ('9th_inning', '4-й Иннинг'),
        ]
    )
    handicap = models.FloatField(null=True, blank=True)
    handicap_team1_odds = models.FloatField(null=True, blank=True)
    handicap_team2_odds = models.FloatField(null=True, blank=True)
    handicap_team1_result = models.CharField(max_length=5, null=True, blank=True)
    handicap_team2_result = models.CharField(max_length=5, null=True, blank=True)

    class Meta():
        db_table = 'mlb_handicap_bet'
        verbose_name = 'Ставка на фору'
        verbose_name_plural = 'Ставки на форы'

class MLBUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)  # Автоматически обновляется при изменении записи

    class Meta:
        db_table = 'mlb_update'
        verbose_name = "Обновление MLB"
        verbose_name_plural = "Обновления MLB"

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
