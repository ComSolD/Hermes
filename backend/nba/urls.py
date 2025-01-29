from django.urls import path

from nba.views import HomePage

app_name = 'nba'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]