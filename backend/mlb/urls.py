from django.urls import path

from mlb import views

app_name = 'mlb'

urlpatterns = [
    path('match/<str:match_id>', views.match, name='match'),
]