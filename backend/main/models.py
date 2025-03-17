from django.db import models

class Tournament(models.Model):
    LEAGUE_CHOICES = [
        ('NBA', 'NBA'),
        ('NHL', 'NHL'),
        ('NFL', 'NFL'),
        ('MLB', 'MLB'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=LEAGUE_CHOICES)
    is_active = models.BooleanField(default=True)  # Чтобы можно было включать/выключать турниры
    order = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['order']  # Сортируем по порядку
        db_table = 'tournament'
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'

    def __str__(self):
        return self.name