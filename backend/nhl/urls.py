from django.urls import path

from nhl import views

app_name = 'nhl'

urlpatterns = [
    path('match/<str:match_id>', views.match_statistic, name='match_statistic'),
    path('match/<str:match_id>/total/<int:period>', views.match_total, name='match_total'),
    path('match/<str:match_id>/moneyline', views.match_moneyline, name='match_moneyline'),
    path('match/<str:match_id>/1x2', views.match_1x2, name='match_1x2'),
    path('match/<str:match_id>/handicap/<int:period>', views.match_handicap, name='match_handicap'),

    path('schedule/', views.schedule, name='schedule'),
    # path('statistic/', views.statistic, name='statistic'),
    # path('filterstat/', views.filter_stat, name='filter_stat'),

]