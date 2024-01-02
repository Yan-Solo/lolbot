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
        I  = 300
        II  = 200
        III  = 100
        IV = 0

    class QueueType(Enum):
        RANKED_FLEX_SR = "Flex"
        RANKED_SOLO_5x5 = "Solo"

    class ANSITextColorCode(Enum):
        Gray = 30
        Red = 31
        Green = 32
        Yellow = 33
        Blue = 34
        Pink = 35
        Cyan = 36 # lightblue
        White = 37