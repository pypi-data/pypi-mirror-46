
_settings = {
    "api_key": '',
    "region": None,
    "api_key_in_header": True
}

_headers = {}

def connect(api_key, region=None, api_key_in_header=True):
    """setup the connection for all following API calls

    Keyword arguments:
    api_key -- string
    region  -- region object (optional)
    """

    _settings["api_key"] = api_key
    _settings["region"] = region
    _settings["api_key_in_header"] = api_key_in_header

    if api_key_in_header:
        _headers["X-Riot-Token"] = _settings["api_key"]


def get_headers():
    return _headers


def get_base_url(region):
    if region is not None:
        _settings["region"] = region

    if _settings["region"] is None:
        raise Exception("region is required.")

    return _settings["region"]["proxy"]["url"]


def get_main_params():
    if not _settings["api_key_in_header"]:
        return {"api_key": _settings["api_key"]}
    return {}