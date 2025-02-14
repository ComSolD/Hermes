from django.contrib import admin

from nba.models import NBATeam, NBAMatch, NBATeamStat, NBATeamPtsStat, NBAPlayer, NBAPlayerStat, NBAMoneylineBet, NBATotalBet, NBASpreadBet, NBAUpdate


admin.site.register(NBATeam)

admin.site.register(NBAMatch)

admin.site.register(NBATeamStat)

admin.site.register(NBATeamPtsStat)

admin.site.register(NBAPlayer)

admin.site.register(NBAPlayerStat)

admin.site.register(NBAMoneylineBet)

admin.site.register(NBATotalBet)

admin.site.register(NBASpreadBet)

admin.site.register(NBAUpdate)

