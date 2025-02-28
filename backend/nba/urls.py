from django.urls import path

from nba import views

app_name = 'nba'

urlpatterns = [
    path('match/<str:match_id>', views.match_statistic, name='match_statistic'),
    path('match/<str:match_id>/total', views.match_total, name='match_total'),
]