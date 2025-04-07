from django.db import models
import uuid

def team_logo_upload_path(instance, filename):
    return f"mlb/team_logos/{instance.team_id}/{filename}"

class NHLTeam(models.Model):

    CONFERENCE_CHOICES = [
        ('Eastern Conference', 'Восточная Конференция'),
        ('Western Conference', 'Западная Конференция')
    ]
    
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    conference = models.CharField(max_length=100, null=True, blank=True, choices=CONFERENCE_CHOICES)
    logo = models.ImageField(
        upload_to=team_logo_upload_path,
        null=True,
        blank=True
    )

    class Meta():
        db_table = 'nhl_team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['name']  # 👈 сортировка по имени

    def __str__(self):
        return self.name  # 👈 отображение в админке

class NHLMatch(models.Model):
    match_id = models.CharField(max_length=200,primary_key=True, editable=False)
    team1 = models.ForeignKey(NHLTeam, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(NHLTeam, related_name='away_matches', on_delete=models.CASCADE)
    status = models.CharField(null=True, blank=True, max_length=20)
    season = models.CharField(max_length=10)
    time = models.TimeField(null=True, blank=True)
    stage = models.CharField(null=True, blank=True, max_length=100,
        choices=[
            ('regular', 'Регулярный сезон'),
            ('preseason', 'Пресезон'),
            ('in-season championship', 'Внутрисезонный финал'),
            ('in-season semifinals', 'Внутрисезонный полуфинал'),
            ('in-season quarterfinals', 'Внутрисезонный четвертьфинал'),
            ('east finals', 'Финал востока'),
            ('west finals', 'Финал запада'),
            ('east semifinals', 'Полуфинал востока'),
            ('west semifinals', 'Полуфинал запада'),
            ('east 1st round', 'Первый раунд востока'),
            ('west 1st round', 'Первый раунд запада'),
            ('stanley cup final', 'Финал Кубка Стенли'),
        ])
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
    total_p1 = models.IntegerField()
    total_p1_missed = models.IntegerField()
    total_p2 = models.IntegerField()
    total_p2_missed = models.IntegerField()
    total_p3 = models.IntegerField()
    total_p3_missed = models.IntegerField()

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

    POSITION_CHOICES = [
        ('forward', 'Нападающий'),
        ('defenseman', 'Защитник'),
        ('goalie', 'Вратарь'),
    ]

    stat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(NHLPlayer, on_delete=models.CASCADE)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, choices=POSITION_CHOICES)
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
    sv_procent = models.FloatField(null = True)
    essv = models.IntegerField(null = True)
    ppsv = models.IntegerField(null = True)

    class Meta():
        db_table = 'nhl_player_stat'
        verbose_name = 'Статистика грока'
        verbose_name_plural = 'Статистика игроков'

class NHLMoneylineBet(models.Model):
    moneyline_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_period', '1-й Период'),
            ('2nd_period', '2-й Период'),
            ('3rd_period', '3-й Период'),
        ]
    )

    team1_odds = models.FloatField(null=True, blank=True)
    team2_odds = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=36, null=True, blank=True)


    class Meta():
        db_table = 'nhl_moneyline_bet'
        verbose_name = 'Ставка на победу'
        verbose_name_plural = 'Ставки на победу'

class NHLXBet(models.Model):
    x_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_period', '1-й Период'),
            ('2nd_period', '2-й Период'),
            ('3rd_period', '3-й Период'),
        ]
    )

    team1_odds = models.FloatField(null=True, blank=True)
    draw = models.FloatField(null=True, blank=True)
    team2_odds = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=36, null=True, blank=True)


    class Meta():
        db_table = 'nhl_x_bet'
        verbose_name = 'Ставка на победу или ничью'
        verbose_name_plural = 'Ставки на победу или ничью'

class NHLTotalBet(models.Model):

    RESULT_CHOICES = [
        ('over', 'Больше'),
        ('draw', 'Равно'),
        ('under', 'Меньше')
    ]

    total_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_period', '1-й Период'),
            ('2nd_period', '2-й Период'),
            ('3rd_period', '3-й Период'),
        ]
    )

    total = models.FloatField()
    over_odds = models.FloatField(null=True, blank=True)
    under_odds = models.FloatField(null=True, blank=True)
    total_result = models.CharField(max_length=10, null=True, blank=True, choices=RESULT_CHOICES)

    class Meta():
        db_table = 'nhl_total_bet'
        verbose_name = 'Ставка на тотал'
        verbose_name_plural = 'Ставки на тоталы'

class NHLHandicapBet(models.Model):

    RESULT_CHOICES = [
        ('win', 'Победа'),
        ('draw', 'Ничья'),
        ('lose', 'Поражение')
    ]

    handicap_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(NHLMatch, on_delete=models.CASCADE)

    period = models.CharField(
        max_length=20, 
        choices=[
            ('full_time', 'Весь Матч'),
            ('1st_period', '1-й Период'),
            ('2nd_period', '2-й Период'),
            ('3rd_period', '3-й Период'),
        ]
    )
    handicap = models.FloatField(null=True, blank=True)
    handicap_team1_odds = models.FloatField(null=True, blank=True)
    handicap_team2_odds = models.FloatField(null=True, blank=True)
    handicap_team1_result = models.CharField(max_length=5, null=True, blank=True, choices=RESULT_CHOICES)
    handicap_team2_result = models.CharField(max_length=5, null=True, blank=True, choices=RESULT_CHOICES)

    class Meta():
        db_table = 'nhl_handicap_bet'
        verbose_name = 'Ставка на фору'
        verbose_name_plural = 'Ставки на форы'

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
