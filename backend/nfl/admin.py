from django.contrib import admin

from nfl.models import NFLTeam, NFLMatch, NFLTeamStat, NFLTeamPtsStat, NFLPlayer, NFLPlayerStat, NFLBet, NFLUpdate


admin.site.register(NFLTeam)

admin.site.register(NFLMatch)

admin.site.register(NFLTeamStat)

admin.site.register(NFLTeamPtsStat)

admin.site.register(NFLPlayer)

admin.site.register(NFLPlayerStat)

admin.site.register(NFLBet)

admin.site.register(NFLUpdate)

