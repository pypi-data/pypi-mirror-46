from . import APIRequest

__VERSION = "v4"


def summoner_by_name(summoner_name, region=None):
    url = '/lol/summoner/{version}/summoners/by-name/{summonerName}'
    api = APIRequest(
        url.format(
            version=__VERSION,
            summonerName=summoner_name
        )
    )
    api.get(region)

    return api
