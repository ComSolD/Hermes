from django.urls import path

from nba import views

app_name = 'nba'

urlpatterns = [
    path('match/<str:match_id>', views.match_statistic, name='match_statistic'),
    path('match/<str:match_id>/total/<int:period>', views.match_total, name='match_total'),
    path('match/<str:match_id>/moneyline', views.match_moneyline, name='match_moneyline'),
    path('match/<str:match_id>/handicap/<int:period>', views.match_handicap, name='match_handicap'),

    path('schedule/', views.schedule, name='schedule'),

    path('filterstat/', views.filter_stat, name='filter_stat'),
    path('seasons_by_filters/', views.seasons_by_filters, name='seasons_by_filters'),
    path('teams_by_filters/', views.teams_by_filters, name='teams_by_filters'),
    path('opponents_by_filters/', views.opponents_by_filters, name='opponents_by_filters'),
    path('stages_by_filters/', views.stages_by_filters, name='stages_by_filters'),


]