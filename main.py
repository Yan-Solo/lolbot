#!/bin/python3


import json
import requests
import schedule
import sys
import time
import yaml
import os

from pprint import pprint
# Local imports
from enums import Enums
from core import Core

Vdebug = False

def debug(valname, val):
    global Vdebug
    if Vdebug:
        print(f"{valname}:")
        if isinstance(val, map):
            pprint(list(val))
        else:
            pprint(val)


def load_config():
    global Vdebug
    print("Loading config..")
    config = {}
    try:
        with open(sys.argv[1], "r") as configFile:
            config = yaml.load(configFile, Loader=yaml.FullLoader)
    except Exception:
        sys.exit("Error loading config!")

    if config.get("debug"):
        Vdebug = True

    debug("config", config)
    print("Done loading config!")
    return config


def writeRankToFile(rank, queue, summonerId):
    path = Core.os_join("tmp",f"{summonerId}.{queue}.rank")
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(rank)


def readRankFromFile(summonerId, queue):
    path = Core.os_join("tmp",f"{summonerId}.{queue}.rank")
    try:
        with open(path, encoding="utf-8", mode="r") as file:
            jsonData = json.loads(file.read())
            return jsonData
    except FileNotFoundError:
        print(f"The rank file for {summonerId}.{queue} doesn't exist yet")
        return None

# Source: https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06
# other: https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51#masked-links
def testingDiscordColorsWithBot():

    print("testing!")

    payload = {
        "content": str(""
            "```ansi\r\n"
            "\u001b[1;41mTesting Discord Bot styling\u001b[0m\r\n"
            "\u001b[1;33mNamingTest\u001b[0m\r\n"
            "\u001b[1;32mPromoted\u001b[0m\r\n"
            "\u001b[1;92mPromoted2\u001b[0m\r\n" # not working
            "\u001b[1;31mDemoted\u001b[0m\r\n"
            "\u001b[1;91mDemoted2\u001b[0m\r\n" # not working
            "\u001b[1;36mLP Change\u001b[0m\r\n"
            "```"
        "")
    }

    print(payload['content'])

    return payload


# TODO make library for coloring/styling all this ...
def createDiscordMessage(discordMessageName, currentRank, oldRank):
    (isTierChanged, isRankChanged, isLpChanged) = getRankChanges(oldRank, currentRank)

    summonerMsg = f"\u001b[1;33m{discordMessageName}\u001b[0m is now "
    message = summonerMsg
    currentRankMsg = f"{currentRank['tier']} {currentRank['rank']} {currentRank['lp']}"
    promotedCurrentRankMsg = f"from {oldRank['tier']} {oldRank['rank']} to \u001b[1;32m{currentRankMsg}\u001b[0m"
    demotedCurrentRankMsg = f"from {oldRank['tier']} {oldRank['rank']} to \u001b[1;31m{currentRankMsg}\u001b[0m"
    
    lpDifference  = calculateLpDifference(oldRank, currentRank)
    blueLpDifferenceMsg = "\u001b[1;36m({lpDifference} lp)\u001b[0m"

    if(isTierChanged):
        isTierPromoted = Enums.LeagueTier[currentRank['tier']].value > Enums.LeagueTier[oldRank['tier']].value
        if(isTierPromoted):
            message = f"Congrats {summonerMsg}\u001b[1;32mpromoted\u001b[0m {promotedCurrentRankMsg} {blueLpDifferenceMsg}"
        else:
            message += f"\u001b[1;31mdemoted\u001b[0m {demotedCurrentRankMsg} {blueLpDifferenceMsg}"

    if(isRankChanged):
        isRankPromoted = Enums.LeagueRank[currentRank['rank']].value > Enums.LeagueRank[oldRank['rank']].value
        if(isRankPromoted):
            message = f"Congrats {summonerMsg}\u001b[1;32mpromoted\u001b[0m {promotedCurrentRankMsg} {blueLpDifferenceMsg}"
        else:
            message += f"\u001b[1;31mdemoted\u001b[0m {demotedCurrentRankMsg} {blueLpDifferenceMsg}"

    if(isLpChanged and not isTierChanged and not isRankChanged):
        if("-" in lpDifference): # TODO this is so bad but lazy
            message += f"{currentRankMsg} \u001b[1;35m({lpDifference} lp)\u001b[0m"
        else:
            message += f"{currentRankMsg} \u001b[1;36m({lpDifference} lp)\u001b[0m"

    print(message)

    payload = {
        "content": (""
            "```ansi\r\n"
            f"{message}"
            "```"        
        "")
    }

    return payload


def postToDiscord(discordMessageName, payload):
    headers = {
        "Content-Type": "application/json"
    }

    discordUrl = (
        "https://discord.com/api/webhooks/1090678079443181650/"
        "jBF_EhBUAG8y-uhRVYO4SeT1VeltFd0YmlN_rAS1jDB5dwRfMkBzG1u5bUJHRo8_clVa"
    )

    response = requests.post(
        discordUrl, data=json.dumps(payload), headers=headers
    )

    if response.status_code == 204:
        print(f"Message for {discordMessageName} sent successfully")
    else:
        print("Failed to send message. Status code:", response.status_code)


def getCurrentRank(riotApiToken, summonerId, queueType):
    riot_api_url = (
        f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
        f"{summonerId}"
    )

    headers = {
        "X-Riot-Token": f"{riotApiToken}"
    }

    response = requests.get(riot_api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for queue in data:
            if queue["queueType"] == queueType:
                rank = {
                    "tier": queue["tier"],
                    "rank": queue["rank"],
                    "lp": queue["leaguePoints"]
                }
                return rank

    else:
        print(f"Error making request to riot for {summonerId}")


def getRankChanges(oldRank, currentRank): 
    isTierChanged = Enums.LeagueTier[currentRank['tier']].value != Enums.LeagueTier[oldRank['tier']].value
    isRankChanged = Enums.LeagueRank[currentRank['rank']].value != Enums.LeagueRank[oldRank['rank']].value
    isLpChanged = oldRank["lp"] != currentRank["lp"]

    return (isTierChanged, isRankChanged, isLpChanged)


def rankChanged(oldRank, currentRank):
    if oldRank is None or currentRank is None:
        return False

    (isTierChanged, isRankChanged, isLpChanged) = getRankChanges(oldRank, currentRank)

    return isTierChanged or isRankChanged or isLpChanged


def calculateLpDifference(oldRank, currentRank):
    oldLpInt = int(oldRank['lp'])
    currentLpInt = int(currentRank['lp'])
    difference = currentLpInt - oldLpInt
    output = f"+ {difference}" if difference > 0 else f"{difference}"
    return output


def main(monitored_players):
    for player in monitored_players:
        summonerId = player['summonerId']
        discordMessageName = player['discordMessageName']
        queue = player['queue']

        oldRank = readRankFromFile(summonerId, queue)
        currentRank = getCurrentRank(riotApiToken, summonerId, queue)
        writeRankToFile(json.dumps(currentRank), queue, summonerId)
        if rankChanged(oldRank, currentRank):
            dicordMessagePayload = createDiscordMessage(discordMessageName, currentRank, oldRank)
            postToDiscord(discordMessageName, dicordMessagePayload)
        else:
            print(f"No changes for {discordMessageName} "
                  f"or file wasn't present")

config = load_config()
riotApiToken = config['riotApiToken']

schedule.every(1).minutes.do(main, config['monitored_players'])

while True:
    schedule.run_pending()
    time.sleep(1)
