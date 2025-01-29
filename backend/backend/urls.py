from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('nba/', include('nba.urls', namespace='nba')),
    path('nfl/', include('nfl.urls', namespace='nfl')),
    path('nhl/', include('nhl.urls', namespace='nhl')),
]
