from enum import Enum

class Enums:
    class LeagueTier(Enum):
        IRON  = 0
        BRONZE  = 400
        SILVER  = 800
        GOLD = 1200
        PLATINUM = 1600
        EMERALD = 2000
        DIAMOND = 2400
        MASTER = 2800
        GRANDMASTER = 3200
        CHALLENGER = 3600

    class LeagueRank(Enum):
        I  = 0
        II  = 100
        III  = 200
        IV = 300