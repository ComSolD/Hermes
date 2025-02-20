from django.contrib import admin

from nhl.models import NHLTeam, NHLMatch, NHLTeamStat, NHLTeamPtsStat, NHLPlayer, NHLPlayerStat, NHLMoneylineBet, NHLXBet, NHLTotalBet, NHLHandicapBet, NHLUpdate


admin.site.register(NHLTeam)

admin.site.register(NHLMatch)

admin.site.register(NHLTeamStat)

admin.site.register(NHLTeamPtsStat)

admin.site.register(NHLPlayer)

admin.site.register(NHLPlayerStat)

admin.site.register(NHLMoneylineBet)

admin.site.register(NHLXBet)

admin.site.register(NHLTotalBet)

admin.site.register(NHLHandicapBet)

admin.site.register(NHLUpdate)
