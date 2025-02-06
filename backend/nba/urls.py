from django.urls import path

from nba import views

from nba.views import HomePage

app_name = 'nba'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('match/<str:match_id>', views.match, name='match'),
]