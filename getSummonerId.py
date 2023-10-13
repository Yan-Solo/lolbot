#!/bin/python3


import datetime
import requests
import sys
import yaml

from pprint import pprint


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
    return config


def getSummonerId():
    summonerName = sys.argv[1]
    api_url = (
        f"https://euw1.api.riotgames.com/lol/summoner/v4"
        f"/summoners/by-name/{summonerName}"
    )
    headers = {
        "X-Riot-Token": "RGAPI-8f07d8e8-d4f9-41ec-b8af-8a78a81835ee",
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        summonerId = data['id']
        print(summonerId)
    else:
        print(f"Request failed with status code {response.status_code}")


getSummonerId()
