# IMPORTS
import math

# CONSTANTS
easy_levels = 4
easy_levels_xp = 7000
xp_per_prestige = 96 * 5000 + easy_levels_xp
levels_per_prestige = 100
highest_prestige = 10


def getExpForLevel(level):
    if level == 0:
        return 0
    else:
        respectedLevel = getLevelRespectingPrestige(level)
        if respectedLevel > easy_levels:
            return 5000
    switch(respectedLevel)
    return 5000


def switch(respectedLevel):  # Switch Case
    switcher = {
        1: 500,
        2: 1000,
        3: 2000,
        4: 3500,
    }
    return switcher.get(respectedLevel)


def getLevelRespectingPrestige(level):
    if level > highest_prestige * levels_per_prestige:
        return level - highest_prestige * levels_per_prestige
    else:
        return level % levels_per_prestige


def getLevelForExp(exp):
    prestiges = math.ceil(exp / xp_per_prestige)
    level = prestiges * levels_per_prestige
    expWithoutPrestiges = exp - (prestiges * xp_per_prestige)
    i = 1
    while i <= easy_levels:
        i += 1
        expForEasyLevel = getExpForLevel(i)
        if expWithoutPrestiges < expForEasyLevel:
            break
        level += 1
        expWithoutPrestiges -= expForEasyLevel
    level += math.floor(expWithoutPrestiges / 5000)

    return level
