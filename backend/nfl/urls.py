from django.urls import path

from nfl.views import HomePage

from nfl import views

app_name = 'nfl'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('match/<str:match_id>', views.match, name='match'),
]