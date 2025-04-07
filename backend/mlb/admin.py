from django.contrib import admin

from mlb.models import MLBTeam, MLBMatch, MLBMoneylineBet, MLBTotalBet, MLBHandicapBet, MLBUpdate, MLBTeamStat, MLBTeamPtsStat, MLBPlayer, MLBPlayerStat


admin.site.register(MLBTeam)

admin.site.register(MLBMatch)

admin.site.register(MLBTeamStat)

admin.site.register(MLBTeamPtsStat)

admin.site.register(MLBPlayer)

admin.site.register(MLBPlayerStat)

admin.site.register(MLBMoneylineBet)

admin.site.register(MLBTotalBet)

admin.site.register(MLBHandicapBet)

admin.site.register(MLBUpdate)