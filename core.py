import os
import requests

# for linux = /
# for windows = c:\\
class Core:
    def rootPath():
        return os.path.abspath(os.sep)

    def OSJoin(*strings):
        path = Core.rootPath()
        for string in strings:
            path = os.path.join(path,string)
        return path
    
    def getLeagueApiResponse(endpoint, riotApiToken, queryParameters="",region="euw1"):
        #league/v4/entries/by-summoner/
        riot_api_url = f"https://{region}.api.riotgames.com/lol/{endpoint}{queryParameters}"
            
        headers = {
            "X-Riot-Token": f"{riotApiToken}"
        }

        response = requests.get(riot_api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error {response.status_code} making request to riot with endpoint {riot_api_url}")
        return None
