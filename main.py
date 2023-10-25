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
        print("Path:", file.name)


def readRankFromFile(summonerId, queue):
    path = Core.os_join("tmp",f"{summonerId}.{queue}.rank")
    try:
        with open(path, encoding="utf-8", mode="r") as file:
            jsonData = json.loads(file.read())
            return jsonData
    except FileNotFoundError:
        print(f"The rank file for {summonerId}.{queue} doesn't exist yet")
        os.makedirs(path)
        return readRankFromFile(summonerId, queue)


def postToDiscord(discordMessageName, rank, lpDifference):
    payload = {
        "content": (
            f"{discordMessageName} is now "
            f"{rank['tier']} {rank['rank']} {rank['lp']} ({lpDifference} lp)"
        )
    }

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


def rankChanged(oldRank, currentRank):
    if oldRank is None or currentRank is None:
        return False
    return oldRank["lp"] != currentRank["lp"]


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
            lpDifference = calculateLpDifference(oldRank, currentRank)
            postToDiscord(discordMessageName, currentRank, lpDifference)
        else:
            print(f"No changes for {discordMessageName} "
                  f"or file wasn't present")

config = load_config()
riotApiToken = config['riotApiToken']

schedule.every(3).seconds.do(main, config['monitored_players'])

while True:
    schedule.run_pending()
    time.sleep(1)
