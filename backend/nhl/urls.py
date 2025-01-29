from django.urls import path

from nhl.views import HomePage

app_name = 'nhl'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]