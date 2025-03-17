from django.urls import path

from mlb import views

app_name = 'mlb'

urlpatterns = [
    path('match/<str:match_id>', views.match_statistic, name='match_statistic'),
    path('match/<str:match_id>/total/<int:period>', views.match_total, name='match_total'),
    path('match/<str:match_id>/moneyline', views.match_moneyline, name='match_moneyline'),
    path('match/<str:match_id>/handicap/<int:period>', views.match_handicap, name='match_handicap'),

    path('schedule/', views.schedule, name='schedule'),
    # path('statistic/', views.statistic, name='statistic'),
    # path('filterstat/', views.filter_stat, name='filter_stat'),
]