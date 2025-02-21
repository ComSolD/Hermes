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

class MLBMoneylineBet(models.Model):
    moneyline_bet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(MLBMatch, on_delete=models.CASCADE)

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
        # models.Index(fields=['player']),
        models.Index(fields=['date']),
    ]
