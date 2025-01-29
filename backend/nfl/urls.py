from django.urls import path

from nfl.views import HomePage

app_name = 'nfl'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]