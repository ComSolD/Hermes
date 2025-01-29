from django.contrib import admin

from nhl.models import NHLTeam, NHLMatch, NHLTeamStat, NHLTeamPtsStat, NHLPlayer, NHLPlayerStat, NHLBet


admin.site.register(NHLTeam)

admin.site.register(NHLMatch)

admin.site.register(NHLTeamStat)

admin.site.register(NHLTeamPtsStat)

admin.site.register(NHLPlayer)

admin.site.register(NHLPlayerStat)

admin.site.register(NHLBet)
