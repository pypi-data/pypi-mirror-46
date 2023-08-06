from . import APIRequest

__VERSION = "v4"


def entries_by_summoner_id(summoner_id, region=None):
    url = '/lol/league/{version}/entries/by-summoner/{encryptedSummonerId}'
    api = APIRequest(
        url.format(
            version=__VERSION,
            encryptedSummonerId=summoner_id
    ))
    api.get(region)

    return api