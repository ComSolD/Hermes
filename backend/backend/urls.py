from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls', namespace='main')),
    path('api/nba/', include('nba.urls', namespace='nba')),
    path('api/nfl/', include('nfl.urls', namespace='nfl')),
    path('api/nhl/', include('nhl.urls', namespace='nhl')),
    path('api/mlb/', include('mlb.urls', namespace='mlb')),
    
] + debug_toolbar_urls()
