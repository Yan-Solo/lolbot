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

    class TeamPosition(Enum):
        TOP = "Top"
        JUNGLE = "Jungle"
        MIDDLE = "Mid"
        BOTTOM = "ADC"
        UTILITY = "Support"
        UNKNOWN  = "Unknown"

    class SummonerId(Enum):
        Piet = "NaK9nxywCB-yR_X6_nR3lSMvwZUUe59vi2Tq5hH8v1z_sCw"
        Dieter = "si-atm7MwA9WJjRg7_kf3H-mWpdCE3m-NJqh5Uup19gjf6Y"
        Michael = "92xv3Ev8DrF6yoUM25v0kGzJ9PKSOd7V9tbVwgpYG1gORJA"
        Simon = "Hvq6N0p5YzfeE3L23EwLSoEC-BJDzvF6sXzGHP1F_VHbnO0"
        Andres = "Z-zwIwHVdSvXvtUqmyisNXiIsABbzpPAmbKwSWuNyv8uqhA"
        AndresAlt = "HnH7csTpBP8voC0fiJMwTmndTFfOYqnVMpmOP6LC3uLLQFdqLbOPxyGjbw"
        Benjamin = "qcUxUydGzk42nq7IW9MrvxT4DKv9D2r1xB3_Gk4Klyd-VsY"
        Dries = "Da36I4f-iKkpyrd6Vd5xIPDML7CUUBHzB1X25y5bzekllIFn"
